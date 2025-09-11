import gradio as gr

from utils import onSystemPromptChanged, userMessage, responseStream
from constants import default_system_prompts


# Helper wrapper to set the systemMessage for the active tab before sending the user message
def userMessage_with_topic(tab_id):
    def _inner(message: str, history: list):
        onSystemPromptChanged(default_system_prompts.get(tab_id, tab_id))
        return userMessage(message, history)

    return _inner


# Now build tabs content below the header row using a builder pattern for easy future custom UIs
def build_generic_tab(tab_id: str):
    with gr.Column():
        chatbot = gr.Chatbot(type="messages")
        msg = gr.Textbox(placeholder="Type your message and press Enter...")
        clear = gr.Button("Clear")
        msg.submit(userMessage_with_topic(tab_id), [msg, chatbot], [msg, chatbot], queue=False).then(
            responseStream, chatbot, chatbot
        )
        clear.click(lambda: None, None, chatbot, queue=False)
        return {"chatbot": chatbot, "msg": msg, "clear": clear}
