import gradio as gr

from tabs.generic_tab import build_generic_tab
from tabs.job_match_tab import build_job_match_tab
from tabs.study_notes_tab import build_study_notes_tab
from utils import onModelChange

with gr.Blocks() as ui:
    selectedModel = "Open AI"
    systemMessage = "You are a comedian that tell jokes."
    contextModelchanged = True

    modelChoices = ["Open AI", "Claude AI", "Gemini AI"]

    systemPromptChoices = [
        "Recipe Recommendation",
        "Study Notes Question And Answer",
        "Basic Job Match Assistant",
        "Simple Code Explainer",
        "Virtual Case Study Creator"
    ]

    with gr.Row(variant="compact"):
        # Left: tabs header placeholder; Right: model selector aligned to the right without background
        with gr.Column(scale=1):
            tabs_header = gr.Tabs()
        with gr.Column(scale=0, min_width=220):
            modelDropdown = gr.Dropdown(
                choices=modelChoices,
                value=modelChoices[0],
                label="Model",
                interactive=True,
                container=False,
                show_label=False
            )
            modelDropdown.input(fn=onModelChange, inputs=modelDropdown)

    custom_tab_builders = {
        "Basic Job Match Assistant": build_job_match_tab,
        "Study Notes Question And Answer": build_study_notes_tab
    }

    with gr.Tabs() as tabs:
        tab_components = {}
        for topic in systemPromptChoices:
            with gr.TabItem(topic):
                builder = custom_tab_builders.get(topic)
                if builder:
                    tab_components[topic] = builder()
                else:
                    tab_components[topic] = build_generic_tab(topic)

ui.launch(share=True)
