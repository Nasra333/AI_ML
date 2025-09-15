"""
UI state management utilities for study notes tab.
Provides helper functions for Gradio component updates and visibility management.
"""
import gradio as gr


def show_component():
    """Return Gradio update to make component visible."""
    return gr.update(visible=True)


def hide_component():
    """Return Gradio update to hide component."""
    return gr.update(visible=False)


def toggle_visibility(show_first: bool):
    """
    Toggle visibility between two components.

    Args:
        show_first: If True, show first component and hide second. If False, vice versa.

    Returns:
        Tuple of Gradio updates for (first_component, second_component)
    """
    if show_first:
        return show_component(), hide_component()
    else:
        return hide_component(), show_component()


def reset_component_value(component_type: str = "textbox", value=""):
    """
    Reset component to default value.

    Args:
        component_type: Type of component (not used in current implementation)
        value: Value to reset to

    Returns:
        Gradio update with reset value
    """
    return gr.update(value=value)