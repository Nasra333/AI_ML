"""
Input phase UI components for study notes tab.
Contains the initial input selection interface and file upload functionality.
"""
import gradio as gr
from ..utils.file_readers import get_supported_file_types


def create_input_phase_ui():
    """
    Create the input phase UI components.
    This function should be called within a Gradio context.

    Returns:
        Dictionary containing all input phase components
    """
    # Create components directly in current Gradio context
    input_phase = gr.Group()

    with input_phase:
        gr.Markdown("### Step 1: Choose how to provide your study notes")

        input_method = gr.Radio(
            choices=["Paste Notes", "Upload File"],
            value="Paste Notes",
            label="Input Method"
        )

        # Conditional inputs
        paste_input = gr.Group()
        with paste_input:
            notes_textbox = gr.Textbox(
                label="Study Notes",
                lines=10,
                placeholder="Paste or type your study notes here..."
            )

        file_input = gr.Group(visible=False)
        with file_input:
            file_upload = gr.File(
                label="Upload Study Notes",
                file_types=get_supported_file_types(),
                type="filepath"
            )

        process_btn = gr.Button("Process Notes", variant="primary", size="lg")

    return {
        "input_phase": input_phase,
        "input_method": input_method,
        "paste_input": paste_input,
        "file_input": file_input,
        "notes_textbox": notes_textbox,
        "file_upload": file_upload,
        "process_btn": process_btn
    }