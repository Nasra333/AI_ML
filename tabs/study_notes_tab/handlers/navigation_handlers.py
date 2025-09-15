"""
Navigation handling logic for study notes tab.
Manages phase transitions, resets, and UI state changes.
"""
import gradio as gr
from ..components.ui_state import show_component, hide_component, reset_component_value


def reset_to_input_phase():
    """
    Reset the entire interface back to input selection phase.

    Returns:
        Tuple of updates for all relevant components
    """
    return (
        "",                           # notes_state
        show_component(),             # input_phase
        hide_component(),             # chat_phase
        reset_component_value("", ""), # notes_textbox
        reset_component_value("", None), # file_upload
        reset_component_value("", "Paste Notes"), # input_method
        reset_component_value("", "")  # question
    )


def clear_chat():
    """
    Clear chat history while keeping current phase.

    Returns:
        Empty list for chat history
    """
    return []


def get_default_input_method():
    """
    Get the default input method.

    Returns:
        Default input method string
    """
    return "Paste Notes"


def get_default_style_options():
    """
    Get default answer style options.

    Returns:
        List of default style options
    """
    return ["Bullet Points"]


def get_default_depth_value():
    """
    Get default depth/detail level.

    Returns:
        Default depth value
    """
    return 3