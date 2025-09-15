import gradio as gr
import os
from PyPDF2 import PdfReader
from docx import Document

from utils import onSystemPromptChanged, userMessage, responseStream
from constants import default_system_prompts


def read_uploaded_file(file_path):
    """Read content from uploaded file supporting multiple formats"""
    if not file_path:
        return ""

    try:
        # Get file extension
        _, ext = os.path.splitext(file_path.lower())

        if ext == '.pdf':
            # Read PDF file
            reader = PdfReader(file_path)
            text = ""
            for page in reader.pages:
                text += page.extract_text() + "\n"
            return text.strip()

        elif ext == '.docx':
            # Read DOCX file
            doc = Document(file_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()

        else:
            # Read plain text files (.txt, .md, etc.)
            with open(file_path, 'r', encoding='utf-8') as f:
                return f.read()

    except Exception as e:
        return f"Error reading file: {str(e)}"


def build_study_notes_tab():
    with gr.Column():
        gr.Markdown("## Study Notes Q&A")

        # State to store processed notes
        notes_state = gr.State("")

        # Input selection phase
        with gr.Group() as input_phase:
            gr.Markdown("### Step 1: Choose how to provide your study notes")
            input_method = gr.Radio(
                choices=["Paste Notes", "Upload File"],
                value="Paste Notes",
                label="Input Method"
            )

            # Conditional inputs
            with gr.Group() as paste_input:
                notes_textbox = gr.Textbox(
                    label="Study Notes",
                    lines=10,
                    placeholder="Paste or type your study notes here..."
                )

            with gr.Group(visible=False) as file_input:
                file_upload = gr.File(
                    label="Upload Study Notes",
                    file_types=[".txt", ".md", ".pdf", ".docx"],
                    type="filepath"
                )

            process_btn = gr.Button("Process Notes", variant="primary", size="lg")

        # Chat phase (initially hidden)
        with gr.Group(visible=False) as chat_phase:
            gr.Markdown("### Ask questions about your study notes")
            with gr.Row():
                question = gr.Textbox(
                    label="Your Question",
                    lines=2,
                    placeholder="Ask a question about the notes...",
                    scale=4
                )
                ask_btn = gr.Button("Ask", variant="primary", scale=1)

            with gr.Row():
                clear = gr.Button("Clear Chat")
                new_notes_btn = gr.Button("New Notes", variant="secondary")

            with gr.Accordion("Options", open=False):
                style = gr.CheckboxGroup(
                    choices=["Bullet Points", "Numbered", "Flashcards"],
                    value=["Bullet Points"],
                    label="Answer Style"
                )
                depth = gr.Slider(minimum=1, maximum=5, value=3, step=1, label="Depth / Detail")

            chatbot = gr.Chatbot(type="messages")

        # Event handlers
        def toggle_input_method(method):
            """Show/hide input methods based on selection"""
            if method == "Paste Notes":
                return gr.update(visible=True), gr.update(visible=False)
            else:
                return gr.update(visible=False), gr.update(visible=True)

        def process_notes(method, notes_text, uploaded_file):
            """Process notes and switch to chat phase"""
            if method == "Paste Notes":
                content = (notes_text or "").strip()
            else:
                content = read_uploaded_file(uploaded_file) if uploaded_file else ""

            if not content:
                gr.Warning("Please provide study notes before proceeding.")
                return (
                    content,  # notes_state
                    gr.update(visible=True),   # input_phase
                    gr.update(visible=False),  # chat_phase
                    ""  # question
                )

            return (
                content,  # notes_state
                gr.update(visible=False),  # input_phase
                gr.update(visible=True),   # chat_phase
                ""  # question
            )

        def reset_to_input():
            """Return to input selection phase"""
            return (
                "",  # notes_state
                gr.update(visible=True),   # input_phase
                gr.update(visible=False),  # chat_phase
                "",  # notes_textbox
                None,  # file_upload
                "Paste Notes",  # input_method
                ""   # question
            )

        def build_qna_prompt(notes_content: str, q: str, style_opts: list, depth_val: int):
            q = (q or "").strip()
            style_txt = ", ".join(style_opts or []) or "Bullet Points"
            return (
                "Using the student's study notes below, answer the question. "
                "Cite key concepts from the notes, avoid fabricating content, and keep it well-structured. "
                f"Prefer style: {style_txt}. Detail level: {depth_val}.\n\n"
                f"Study Notes:\n{notes_content}\n\nQuestion:\n{q}"
            )

        def on_ask(notes_content: str, q: str, style_opts: list, depth_val: int, history: list):
            if not notes_content:
                gr.Warning("No study notes available. Please process notes first.")
                return q, history

            onSystemPromptChanged(
                default_system_prompts.get("Study Notes Question And Answer", "Study Notes Question And Answer")
            )
            prompt = build_qna_prompt(notes_content, q, style_opts, depth_val)
            return userMessage(prompt, history)

        # Wire up events
        input_method.change(
            toggle_input_method,
            inputs=[input_method],
            outputs=[paste_input, file_input]
        )

        process_btn.click(
            process_notes,
            inputs=[input_method, notes_textbox, file_upload],
            outputs=[notes_state, input_phase, chat_phase, question]
        )

        ask_btn.click(
            on_ask,
            inputs=[notes_state, question, style, depth, chatbot],
            outputs=[question, chatbot],
            queue=False
        ).then(
            responseStream,
            inputs=[chatbot],
            outputs=[chatbot]
        )

        clear.click(lambda: None, outputs=[chatbot], queue=False)

        new_notes_btn.click(
            reset_to_input,
            outputs=[notes_state, input_phase, chat_phase, notes_textbox, file_upload, input_method, question]
        )

        return {
            "chatbot": chatbot,
            "ask_btn": ask_btn,
            "clear": clear,
            "question": question,
            "notes_state": notes_state
        }
