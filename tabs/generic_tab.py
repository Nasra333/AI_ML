import gradio as gr

from utils import onSystemPromptChanged, userMessage, responseStream
from constants import default_system_prompts


# Now build tabs content below the header row using a builder pattern for easy future custom UIs
def build_generic_tab(tab_id: str):
    with gr.Column():
        chatbot = gr.Chatbot(type="messages")
        msg = gr.Textbox(placeholder="Type your message and press Enter...")
        clear = gr.Button("Clear")
        
        # Set system prompt once when tab is built
        system_prompt = default_system_prompts.get(tab_id, tab_id)
        
        def handle_message(message: str, history: list):
            """Handle user message and add to history"""
            if not message.strip():
                return "", history
            
            # Add user message to history
            updated_history = history + [{"role": "user", "content": message}]
            return "", updated_history
        
        def get_response(history: list):
            """Get AI response with system prompt"""
            if not history:
                return history
            
            # Build messages with system prompt
            messages = [{"role": "system", "content": system_prompt}] + history
            
            # Stream response
            for ai_history in responseStream(messages):
                # Combine history with AI response
                yield history + [ai_history[-1]]
        
        msg.submit(handle_message, [msg, chatbot], [msg, chatbot], queue=False).then(
            get_response, chatbot, chatbot
        )
        clear.click(lambda: None, None, chatbot, queue=False)
        return {"chatbot": chatbot, "msg": msg, "clear": clear}
