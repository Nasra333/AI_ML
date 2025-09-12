import gradio as gr

from utils import onSystemPromptChanged, userMessage, responseStream
from constants import default_system_prompts


def build_study_notes_tab():
    with gr.Column():
        gr.Markdown("## Study Notes Q&A")
        with gr.Row():
            notes = gr.Textbox(label="Study Notes", lines=10, placeholder="Paste or type your study notes here...")
        with gr.Row():
            question = gr.Textbox(label="Your Question", lines=2, placeholder="Ask a question about the notes...")
            ask_btn = gr.Button("Ask", variant="primary")
            clear = gr.Button("Clear")
        with gr.Accordion("Options", open=False):
            style = gr.CheckboxGroup(choices=["Bullet Points", "Numbered", "Flashcards"], value=["Bullet Points"],
                                     label="Answer Style")
            depth = gr.Slider(minimum=1, maximum=5, value=3, step=1, label="Depth / Detail")
        chatbot = gr.Chatbot(type="messages")

        def build_qna_prompt(n: str, q: str, style_opts: list, depth_val: int):
            n = (n or "").strip()
            q = (q or "").strip()
            style_txt = ", ".join(style_opts or []) or "Bullet Points"
            return (
                "Using the student's study notes below, answer the question. "
                "Cite key concepts from the notes, avoid fabricating content, and keep it well-structured. "
                f"Prefer style: {style_txt}. Detail level: {depth_val}.\n\n"
                f"Study Notes:\n{n}\n\nQuestion:\n{q}"
            )

        def on_ask(n: str, q: str, style_opts: list, depth_val: int, history: list):
            onSystemPromptChanged(
                default_system_prompts.get("Study Notes Question And Answer", "Study Notes Question And Answer"))
            prompt = build_qna_prompt(n, q, style_opts, depth_val)
            return userMessage(prompt, history)

        ask_btn.click(on_ask, [notes, question, style, depth, chatbot], [question, chatbot], queue=False).then(
            responseStream, chatbot, chatbot
        )
        clear.click(lambda: None, None, chatbot, queue=False)
        return {"chatbot": chatbot, "ask_btn": ask_btn, "clear": clear, "notes": notes, "question": question}
