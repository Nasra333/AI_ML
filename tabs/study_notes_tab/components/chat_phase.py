"""
Chat phase UI components for study notes tab.
Contains the Q&A interface, options, and chat functionality.
"""
import gradio as gr


def create_chat_phase_ui():
    """
    Create the chat phase UI components.
    This function should be called within a Gradio context.

    Returns:
        Dictionary containing all chat phase components
    """
    # Create components directly in current Gradio context
    chat_phase = gr.Group(visible=False)

    with chat_phase:
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

    return {
        "chat_phase": chat_phase,
        "question": question,
        "ask_btn": ask_btn,
        "clear": clear,
        "new_notes_btn": new_notes_btn,
        "style": style,
        "depth": depth,
        "chatbot": chatbot
    }