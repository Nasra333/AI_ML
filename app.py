import gradio as gr

from constants import (
    TAB_JOB_MATCH,
    TAB_STUDY_NOTES,
    TAB_NAMES,
    modelChoices,
    MODEL_OPEN_AI,
)
from tabs.generic_tab import build_generic_tab
from tabs.job_match_tab import build_job_match_tab
from tabs.study_notes_tab import build_study_notes_tab
from utils import onModelChange

with gr.Blocks(css="#job-match-result { border: 1px solid #e0e0e0; padding: 1rem; border-radius: 0.5rem; }") as demo:
    selectedModel = "Open AI"
    systemMessage = "You are a comedian that tell jokes."
    contextModelchanged = True

    with gr.Row(variant="compact"):
        # Left: tabs header placeholder; Right: model selector aligned to the right without background
        with gr.Column(scale=1):
            tabs_header = gr.Tabs()
        with gr.Column(scale=0, min_width=220):
            modelDropdown = gr.Dropdown(
                choices=modelChoices,
                value=MODEL_OPEN_AI,
                label="Model",
                interactive=True,
                container=False,
                show_label=False,
            )
            modelDropdown.input(fn=onModelChange, inputs=modelDropdown)

    custom_tab_builders = {
        TAB_JOB_MATCH: build_job_match_tab,
        TAB_STUDY_NOTES: build_study_notes_tab,
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

demo.launch(share=True)
