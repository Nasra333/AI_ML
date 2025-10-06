import gradio as gr
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup
import logging

from utils import onSystemPromptChanged, responseStream, openai
from constants import TAB_JOB_MATCH, default_system_prompts, default_tab_titles

# Configure logger
logger = logging.getLogger(__name__)


def build_job_match_tab():
    with gr.Column():
        gr.Markdown(
            "## " + default_tab_titles.get(TAB_JOB_MATCH, 'Job Match Assistant'))
        with gr.Column():
            job_input_type = gr.Radio(
                choices=["Job URL", "Paste Description"],
                value="Job URL",
                label="Job Description"
            )
            job_desc_url = gr.Textbox(label="Job Description URL", lines=1,
                                      placeholder="Enter the URL of the job page...", show_label=False)
            job_desc_text = gr.Textbox(label="Job Description", lines=8,
                                       placeholder="Paste the job description here...", visible=False, show_label=False)
        with gr.Column():
            resume_input_type = gr.Radio(
                choices=["Paste Resume", "Upload PDF"],
                value="Paste Resume",
                label="Resume"
            )
            resume_text = gr.Textbox(label="Candidate Resume/Skills", lines=8,
                                     placeholder="Paste the resume or list key skills here...", show_label=False)
            resume_file = gr.File(label="Upload Resume PDF", file_types=[
                                  ".pdf"], visible=False, show_label=False)
        with gr.Row():
            match_btn = gr.Button("Match Candidate to Job", variant="primary")
            clear = gr.Button("Clear")
        result_box = gr.Chatbot(type="messages", label="Match Result",
                                elem_id="job-match-result")

        def build_match_prompt(jd: str, cv: str):
            jd = jd or ""
            cv = cv or ""
            return (
                "Please analyze the following job description and candidate profile. "
                "Strip out and ignore other information in the job description content that are not relevant. "
                f"Provide: 1) Match score (0-100) 2) Key matching skills 3) Gaps and suggestions 4) Missing keywords that should be included in the resume 5) A brief tailored summary."
                f"\n\nJob Description:\n{jd}\n\nCandidate Profile:\n{cv}"
            )

        def extract_text_from_pdf(pdf_file):
            try:
                reader = PdfReader(pdf_file)
                text = ""
                for page in reader.pages:
                    text += page.extract_text()
                return text
            except Exception as e:
                return f"Error reading PDF: {e}"

        def extract_job_description_from_url_with_ai(url):
            try:
                response = requests.get(url)
                response.raise_for_status()
                soup = BeautifulSoup(response.text, 'html.parser')
                # Extract all text from the page
                page_content = soup.get_text(separator="\n", strip=True)
                return page_content
            except Exception as e:
                return f"Error fetching job description: {e}"

        def on_match(job_input_method: str, url: str, job_text: str, resume_input_type: str, resume_content, resume_file, history: list):
            system_prompt = default_system_prompts.get(
                TAB_JOB_MATCH, "You are a job match assistant")
            onSystemPromptChanged(system_prompt)

            # Initialize history if None
            if history is None:
                history = []

            try:
                # Get job description based on input method
                if job_input_method == "Job URL":
                    jd = extract_job_description_from_url_with_ai(url)
                else:  # "Paste Description"
                    jd = job_text or ""

                if resume_input_type == "Upload PDF" and resume_file is not None:
                    cv = extract_text_from_pdf(resume_file.name)
                else:
                    cv = resume_content or ""

                prompt = build_match_prompt(jd, cv)

                # Add user message to history with context
                job_summary = f"Job from URL: {url}" if job_input_method == "Job URL" else "Pasted job description"
                resume_summary = "Uploaded PDF resume" if resume_input_type == "Upload PDF" else "Pasted resume"
                updated_history = history + \
                    [{"role": "user", "content": f"Analyze job match for {job_summary} and {resume_summary}."}]
                yield updated_history

                # Build messages for AI with system prompt and full context
                messages = [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt}
                ]

                # Stream AI response and update history with error handling
                try:
                    for ai_history in responseStream(messages):
                        # Combine display history with AI response
                        yield updated_history + [ai_history[-1]]
                except Exception as stream_error:
                    # Log the streaming error
                    logger.error(
                        f"Error during AI response streaming: {stream_error}", exc_info=True)

                    # Provide user-facing error message
                    error_message = {
                        "role": "assistant",
                        "content": f"⚠️ An error occurred while generating the response: {str(stream_error)}\n\nPlease try again or contact support if the issue persists."
                    }
                    yield updated_history + [error_message]

                    # Stop the generator after error
                    return

            except Exception as e:
                # Log the general error
                logger.error(
                    f"Error in job match processing: {e}", exc_info=True)

                # Provide user-facing error message
                error_message = {
                    "role": "assistant",
                    "content": f"⚠️ An error occurred while processing your request: {str(e)}\n\nPlease check your inputs and try again."
                }
                yield history + [error_message]

                # Stop the generator after error
                return

        def toggle_job_input(input_method):
            return gr.update(visible=(input_method == "Job URL")), gr.update(visible=(input_method == "Paste Description"))

        def toggle_resume_input(input_type):
            return gr.update(visible=(input_type == "Paste Resume")), gr.update(visible=(input_type == "Upload PDF"))

        job_input_type.change(toggle_job_input, inputs=[job_input_type], outputs=[
                              job_desc_url, job_desc_text])
        resume_input_type.change(toggle_resume_input, inputs=[
                                 resume_input_type], outputs=[resume_text, resume_file])

        match_btn.click(on_match, [job_input_type, job_desc_url, job_desc_text,
                        resume_input_type, resume_text, resume_file, result_box], result_box)

        clear.click(lambda: None,
                    None, [result_box], queue=False)
        return {"result_box": result_box, "match_btn": match_btn, "clear": clear, "job_input_type": job_input_type, "job_desc_url": job_desc_url, "job_desc_text": job_desc_text, "resume_input_type": resume_input_type, "resume_text": resume_text, "resume_file": resume_file}
