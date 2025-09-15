"""
Study Notes Tab Module

Enhanced modular implementation with modern styling, improved UX, and extensible architecture.
Provides document upload/paste functionality with AI-powered Q&A capabilities.
"""
import gradio as gr
from utils import responseStream

# Import enhanced components
from .components.input_phase import create_enhanced_input_phase_ui, get_input_phase_css
from .components.chat_phase import create_enhanced_chat_phase_ui, get_chat_phase_css
from .components.quick_actions import create_quick_actions_css

# Import styling system
from .styles.components import get_component_css
from .styles.theme import get_css_variables

# Import handlers (legacy compatibility maintained)
from .handlers.input_handlers import toggle_input_method, process_notes
from .handlers.chat_handlers import handle_question_clean_ui, get_ai_response_with_context
from .handlers.navigation_handlers import reset_to_input_phase

# Configuration
from .config.ui_config import get_ui_config, validate_config


def build_study_notes_tab():
    """
    Build and configure the enhanced study notes tab with modern styling and improved UX.

    Returns:
        Dictionary containing all tab components for external access
    """
    # Validate configuration
    config_errors = validate_config()
    if config_errors:
        gr.Warning(f"Configuration errors: {', '.join(config_errors)}")

    # Inject CSS styles
    _inject_styles()

    with gr.Column(elem_classes=["study-notes-main-container"]):
        # Modern header with gradient background
        gr.HTML("""
            <div class="study-notes-header">
                <h1>📚 Study Notes Q&A</h1>
                <p>Transform your study materials into an interactive learning experience</p>
            </div>
        """, elem_classes=["main-header"])

        # State management
        notes_state = gr.State("")
        ai_context_state = gr.State("")

        # Create enhanced UI components
        input_components = create_enhanced_input_phase_ui()
        chat_components = create_enhanced_chat_phase_ui()

        # Wire up event handlers (enhanced)
        _setup_enhanced_event_handlers(input_components, chat_components, notes_state, ai_context_state)

        # Return comprehensive component dictionary
        return {
            # Core components (legacy compatibility)
            "chatbot": chat_components["chatbot"],
            "ask_btn": chat_components["ask_btn"],
            "clear": chat_components["clear"],
            "question": chat_components["question"],
            "notes_state": notes_state,
            "ai_context_state": ai_context_state,

            # Enhanced components
            "input_components": input_components,
            "chat_components": chat_components,
            "quick_manager": chat_components.get("quick_manager"),
            "loading_indicator": chat_components.get("loading_indicator"),
            "status_message": chat_components.get("status_message"),

            # Configuration access
            "ui_config": get_ui_config(),
        }


def _inject_styles():
    """Inject all CSS styles for the study notes tab."""
    combined_css = f"""
        {get_css_variables()}
        {get_component_css()}
        {get_input_phase_css()}
        {get_chat_phase_css()}
        {create_quick_actions_css()}
        {_get_main_container_css()}
    """

    gr.HTML(f"<style>{combined_css}</style>", visible=False)


def _get_main_container_css() -> str:
    """Get CSS for the main container and header."""
    return """
    /* Main container styles */
    .study-notes-main-container {
        max-width: 1200px !important;
        margin: 0 auto !important;
        padding: var(--spacing-lg) !important;
    }

    .study-notes-header {
        text-align: center !important;
        background: linear-gradient(135deg, var(--color-primary)10, var(--color-secondary)10) !important;
        border-radius: var(--radius-xl) !important;
        padding: var(--spacing-2xl) !important;
        margin-bottom: var(--spacing-2xl) !important;
        border: 1px solid var(--color-gray-200) !important;
    }

    .study-notes-header h1 {
        color: var(--color-gray-800) !important;
        font-size: var(--font-sizes-2xl) !important;
        font-weight: var(--font-weights-bold) !important;
        margin-bottom: var(--spacing-sm) !important;
        background: linear-gradient(135deg, var(--color-primary), var(--color-secondary)) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        background-clip: text !important;
    }

    .study-notes-header p {
        color: var(--color-gray-600) !important;
        font-size: var(--font-sizes-lg) !important;
        margin: 0 !important;
        font-weight: var(--font-weights-medium) !important;
    }

    /* Responsive header */
    @media (max-width: 768px) {
        .study-notes-main-container {
            padding: var(--spacing-md) !important;
        }

        .study-notes-header {
            padding: var(--spacing-xl) !important;
            margin-bottom: var(--spacing-xl) !important;
        }

        .study-notes-header h1 {
            font-size: var(--font-sizes-xl) !important;
        }

        .study-notes-header p {
            font-size: var(--font-sizes-base) !important;
        }
    }
    """


def _setup_enhanced_event_handlers(input_components: dict, chat_components: dict, notes_state: gr.State, ai_context_state: gr.State):
    """
    Configure enhanced event handlers with improved UX and error handling.

    Args:
        input_components: Dictionary of input phase UI components
        chat_components: Dictionary of chat phase UI components
        notes_state: Gradio state for storing processed notes
        ai_context_state: Gradio state for storing AI context
    """
    # Input method toggle with enhanced visual feedback
    input_components["input_method"].change(
        toggle_input_method,
        inputs=[input_components["input_method"]],
        outputs=[input_components["paste_input"], input_components["file_input"]]
    )

    # Enhanced process notes with loading states
    input_components["process_btn"].click(
        _handle_process_start,
        outputs=[input_components.get("processing_indicator", gr.HTML())],
        queue=False
    ).then(
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
    ).then(
        _handle_process_complete,
        outputs=[input_components.get("processing_indicator", gr.HTML())],
        queue=False
    )

    # Enhanced question handling with loading feedback
    chat_components["ask_btn"].click(
        _handle_question_start,
        outputs=[chat_components.get("loading_indicator", gr.HTML())],
        queue=False
    ).then(
        handle_question_clean_ui,
        inputs=[
            notes_state,
            chat_components["question"],
            chat_components["style"],
            chat_components["depth"],
            chat_components["chatbot"],
            ai_context_state
        ],
        outputs=[
            chat_components["question"],
            chat_components["chatbot"],
            ai_context_state
        ],
        queue=False
    ).then(
        get_ai_response_with_context,
        inputs=[chat_components["chatbot"], ai_context_state],
        outputs=[chat_components["chatbot"], ai_context_state]
    ).then(
        _handle_question_complete,
        outputs=[chat_components.get("loading_indicator", gr.HTML())],
        queue=False
    )

    # Enhanced clear chat with confirmation
    chat_components["clear"].click(
        lambda: (None, "", gr.update(visible=False)),
        outputs=[
            chat_components["chatbot"],
            ai_context_state,
            chat_components.get("status_message", gr.HTML())
        ],
        queue=False
    )

    # Enhanced reset with comprehensive state clearing
    chat_components["new_notes_btn"].click(
        lambda: (
            "",  # notes_state
            gr.update(visible=True),   # input_phase
            gr.update(visible=False),  # chat_phase
            "",  # notes_textbox
            None,  # file_upload
            "Paste Notes",  # input_method
            "",  # question
            "",  # ai_context_state
            gr.update(visible=False),  # status_message
            gr.update(visible=False),  # loading_indicator
        ),
        outputs=[
            notes_state,
            input_components["input_phase"],
            chat_components["chat_phase"],
            input_components["notes_textbox"],
            input_components["file_upload"],
            input_components["input_method"],
            chat_components["question"],
            ai_context_state,
            chat_components.get("status_message", gr.HTML()),
            chat_components.get("loading_indicator", gr.HTML()),
        ]
    )

    # Quick actions are handled by the QuickActionsPanel automatically
    # No need for manual event binding - it's done in the component


def _handle_process_start():
    """Show processing indicator."""
    return gr.update(visible=True)


def _handle_process_complete():
    """Hide processing indicator."""
    return gr.update(visible=False)


def _handle_question_start():
    """Show question loading indicator."""
    return gr.update(visible=True)


def _handle_question_complete():
    """Hide question loading indicator."""
    return gr.update(visible=False)


# Legacy function for backward compatibility
def _setup_event_handlers(input_components: dict, chat_components: dict, notes_state: gr.State, ai_context_state: gr.State):
    """Legacy event handler setup for backward compatibility."""
    return _setup_enhanced_event_handlers(input_components, chat_components, notes_state, ai_context_state)