"""
Input handling logic for study notes tab.
Manages input method selection, file processing, and phase transitions.
"""
import gradio as gr
from ..utils.file_readers import read_uploaded_file
from ..components.ui_state import show_component, hide_component


def toggle_input_method(method: str):
    """
    Show/hide input methods based on selection.

    Args:
        method: Selected input method ("Paste Notes" or "Upload File")

    Returns:
        Tuple of Gradio updates for (paste_input, file_input)
    """
    if method == "Paste Notes":
        return show_component(), hide_component()
    else:
        return hide_component(), show_component()


def process_notes(method: str, notes_text: str, uploaded_file):
    """
    Process notes and switch to chat phase.

    Args:
        method: Input method selected
        notes_text: Text from textbox if paste method
        uploaded_file: File object if upload method

    Returns:
        Tuple of updates for (notes_state, input_phase, chat_phase, question)
    """
    if method == "Paste Notes":
        content = (notes_text or "").strip()
    else:
        content = read_uploaded_file(uploaded_file) if uploaded_file else ""

    if not content:
        gr.Warning("Please provide study notes before proceeding.")
        return (
            content,           # notes_state
            show_component(),  # input_phase
            hide_component(),  # chat_phase
            ""                 # question
        )

    return (
        content,          # notes_state
        hide_component(), # input_phase
        show_component(), # chat_phase
        ""                # question
    )


def validate_notes_content(content: str) -> bool:
    """
    Validate that notes content is not empty.

    Args:
        content: Notes content to validate

    Returns:
        True if content is valid, False otherwise
    """
    return bool(content and content.strip())