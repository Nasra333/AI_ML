import os

import gradio as gr
from dotenv import load_dotenv

from constants import TAB_JOB_MATCH, TAB_NAMES, TAB_SMART_CV, TAB_STUDY_NOTES
from tabs.generic_tab import build_generic_tab
from tabs.job_match_tab import build_job_match_tab
from tabs.smart_cv.app import build_ui
from tabs.study_notes_tab import build_study_notes_tab

# Load environment variables
load_dotenv()

with gr.Blocks(
    css="#job-match-result { border: 1px solid #e0e0e0; padding: 1rem; border-radius: 0.5rem; }"
) as demo:
    selectedModel = "Open AI"
    systemMessage = "You are a useful AI utility buddy."
    contextModelchanged = True

    with gr.Row():
        gr.Markdown(
            """
        # Your Personal Assistant - Zeno
        ### What can I help you with today?
        """
        )

    with gr.Row():
        tabs_header = gr.Tabs()

    custom_tab_builders = {
        TAB_JOB_MATCH: build_job_match_tab,
        TAB_STUDY_NOTES: build_study_notes_tab,
        TAB_SMART_CV: build_ui,
    }
    with gr.Tabs() as tabs:
        tab_components = {}
        for tab_id, tab_name in TAB_NAMES.items():
            with gr.TabItem(tab_name):
                builder = custom_tab_builders.get(tab_id)
                if builder:
                    tab_components[tab_id] = builder()
                else:
                    tab_components[tab_id] = build_generic_tab(tab_id)

if __name__ == "__main__":
    # Get configuration from environment variables
    server_name = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
    server_port = int(os.getenv("PORT", "7860"))

    # Launch with production-ready settings
    demo.launch(
        server_name=server_name,
        server_port=server_port,
        share=False,  # Disable share in production
    )
