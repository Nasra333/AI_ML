import gradio as gr
from PyPDF2 import PdfReader
import requests
from bs4 import BeautifulSoup

from utils import onSystemPromptChanged, askAI, streamAIResponse
from constants import TAB_JOB_MATCH, default_system_prompts


def build_job_match_tab():
    with gr.Column():
        gr.Markdown("## Basic Job Match Assistant")
        with gr.Row():
            job_desc_url = gr.Textbox(label="Job Description URL", lines=1, placeholder="Enter the URL of the job page...")
        with gr.Row():
            resume_input_type = gr.Radio(
                choices=["Paste Resume", "Upload PDF"],
                value="Paste Resume",
                label="Resume Input Type"
            )
        with gr.Row():
            resume_text = gr.Textbox(label="Candidate Resume/Skills", lines=8,
                                     placeholder="Paste the resume or list key skills here...")
            resume_file = gr.File(label="Upload Resume PDF", file_types=[".pdf"], visible=False)
        with gr.Row():
            match_btn = gr.Button("Match Candidate to Job", variant="primary")
            clear = gr.Button("Clear")
        result_box = gr.Markdown(label="Match Result", visible=False)

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
                page_content = soup.get_text(separator="\n", strip=True)  # Extract all text from the page
                return page_content
                # # Use AI to analyze the page content and extract the job description
                # ai_prompt = (
                #     "You are an AI assistant. Analyze the following webpage content and extract the job description. "
                #     "If no job description is found, respond with 'No job description found.'\n\n"
                #     f"Webpage Content:\n{page_content}"
                # )
                # job_desc = askAI(ai_prompt)  # Assuming `askAI` sends the prompt to the AI model and returns the response
                # return job_desc
            except Exception as e:
                return f"Error fetching job description: {e}"


        def on_match(url: str, input_type: str, resume_content, resume_file):
            system_prompt = default_system_prompts.get(TAB_JOB_MATCH, "You are a job match assistant, who takes job description and candidate resume and provides a match score, key matching skills, gaps and suggestions, and a brief tailored summary.")
            onSystemPromptChanged(system_prompt)
            
            yield gr.update(visible=True, value="Processing...")

            jd = extract_job_description_from_url_with_ai(url)
            
            if input_type == "Upload PDF" and resume_file is not None:
                cv = extract_text_from_pdf(resume_file.name)
            else:
                cv = resume_content or ""
            
            prompt = build_match_prompt(jd, cv)

            print(f"User Prompt: {prompt}")
            
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ]
            
            
            for chunk in streamAIResponse(messages):
                yield chunk

        def toggle_resume_input(input_type):
            return gr.update(visible=(input_type == "Paste Resume")), gr.update(visible=(input_type == "Upload PDF"))

        resume_input_type.change(toggle_resume_input, inputs=[resume_input_type], outputs=[resume_text, resume_file])

        match_btn.click(on_match, [job_desc_url, resume_input_type, resume_text, resume_file], result_box)
        
        clear.click(lambda: gr.update(value="", visible=False), None, result_box, queue=False)
        return {"result_box": result_box, "match_btn": match_btn, "clear": clear, "job_desc_url": job_desc_url, "resume_input_type": resume_input_type, "resume_text": resume_text, "resume_file": resume_file}
