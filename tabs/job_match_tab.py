import gradio as gr

from utils import onSystemPromptChanged, userMessage, responseStream
from constants import default_system_prompts


def build_job_match_tab():
    with gr.Column():
        gr.Markdown("## Basic Job Match Assistant")
        with gr.Row():
            job_desc = gr.Textbox(label="Job Description", lines=8, placeholder="Paste the job description here...")
            resume = gr.Textbox(label="Candidate Resume/Skills", lines=8,
                                placeholder="Paste the resume or list key skills here...")
        with gr.Row():
            match_btn = gr.Button("Match Candidate to Job", variant="primary")
            clear = gr.Button("Clear")
        chatbot = gr.Chatbot(type="messages")

        def build_match_prompt(jd: str, cv: str):
            jd = jd or ""
            cv = cv or ""
            return f"Please analyze the following job description and candidate profile. Provide: 1) Match score (0-100) 2) Key matching skills 3) Gaps and suggestions 4) A brief tailored summary.\n\nJob Description:\n{jd}\n\nCandidate Profile:\n{cv}"

        def on_match(jd: str, cv: str, history: list):
            onSystemPromptChanged(default_system_prompts.get("Basic Job Match Assistant", "Basic Job Match Assistant"))
            prompt = build_match_prompt(jd, cv)
            return userMessage(prompt, history)

        match_btn.click(on_match, [job_desc, resume, chatbot], [job_desc, chatbot], queue=False).then(
            responseStream, chatbot, chatbot
        )
        clear.click(lambda: None, None, chatbot, queue=False)
        return {"chatbot": chatbot, "match_btn": match_btn, "clear": clear, "job_desc": job_desc, "resume": resume}
