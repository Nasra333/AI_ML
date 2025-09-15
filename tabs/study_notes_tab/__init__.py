"""
Study Notes Tab Module

A refactored modular implementation of the study notes tab with clean separation of concerns.
Provides document upload/paste functionality with AI-powered Q&A capabilities.
"""
import gradio as gr
from utils import responseStream

# Import components
from .components.input_phase import create_input_phase_ui
from .components.chat_phase import create_chat_phase_ui

# Import handlers
from .handlers.input_handlers import toggle_input_method, process_notes
from .handlers.chat_handlers import handle_question_clean_ui, get_ai_response_with_context
from .handlers.navigation_handlers import reset_to_input_phase


def build_study_notes_tab():
    """
    Build and configure the study notes tab with all its components and event handlers.

    Returns:
        Dictionary containing all tab components for external access
    """
    with gr.Column():
        gr.Markdown("## Study Notes Q&A")

        # State to store processed notes
        notes_state = gr.State("")

        # Create UI phases
        input_components = create_input_phase_ui()
        chat_components = create_chat_phase_ui()

        # Wire up event handlers
        _setup_event_handlers(input_components, chat_components, notes_state)

        # Return components for external access
        return {
            "chatbot": chat_components["chatbot"],
            "ask_btn": chat_components["ask_btn"],
            "clear": chat_components["clear"],
            "question": chat_components["question"],
            "notes_state": notes_state
        }


def _setup_event_handlers(input_components: dict, chat_components: dict, notes_state: gr.State):
    """
    Configure all event handlers for the study notes tab.

    Args:
        input_components: Dictionary of input phase UI components
        chat_components: Dictionary of chat phase UI components
        notes_state: Gradio state for storing processed notes
    """
    # Input method toggle
    input_components["input_method"].change(
        toggle_input_method,
        inputs=[input_components["input_method"]],
        outputs=[input_components["paste_input"], input_components["file_input"]]
    )

    # Process notes and switch phases
    input_components["process_btn"].click(
        process_notes,
        inputs=[
            input_components["input_method"],
            input_components["notes_textbox"],
            input_components["file_upload"]
        ],
        outputs=[
            notes_state,
            input_components["input_phase"],
            chat_components["chat_phase"],
            chat_components["question"]
        ]
    )

    # Handle questions with clean UI
    chat_components["ask_btn"].click(
        handle_question_clean_ui,
        inputs=[
            notes_state,
            chat_components["question"],
            chat_components["style"],
            chat_components["depth"],
            chat_components["chatbot"]
        ],
        outputs=[
            chat_components["question"],
            chat_components["chatbot"]
        ],
        queue=False
    ).then(
        get_ai_response_with_context,
        inputs=[chat_components["chatbot"]],
        outputs=[chat_components["chatbot"]]
    )

    # Clear chat
    chat_components["clear"].click(
        lambda: None,
        outputs=[chat_components["chatbot"]],
        queue=False
    )

    # Reset to input phase
    chat_components["new_notes_btn"].click(
        reset_to_input_phase,
        outputs=[
            notes_state,
            input_components["input_phase"],
            chat_components["chat_phase"],
            input_components["notes_textbox"],
            input_components["file_upload"],
            input_components["input_method"],
            chat_components["question"]
        ]
    )