"""
Enhanced chat phase UI components for study notes tab.
Features improved styling, better organization, and enhanced UX.
"""
import gradio as gr
from typing import Dict, List, Tuple
from ..styles.components import (
    styled_chatbot, styled_textbox, styled_button, styled_row,
    styled_column, styled_group, styled_accordion, create_section_header,
    create_loading_indicator, create_status_message
)
from ..components.quick_actions import create_quick_actions_panel
from ..config.ui_config import CHAT_CONFIG, OPTIONS_CONFIG


def create_enhanced_chat_phase_ui() -> Dict[str, any]:
    """
    Create the enhanced chat phase UI with improved styling and organization.
    This function should be called within a Gradio context.

    Returns:
        Dictionary containing all chat phase components
    """
    # Create main chat phase container
    chat_phase = styled_group(variant="default", visible=False)

    with chat_phase:
        # Section header with improved typography
        create_section_header(
            "Ask questions about your study notes",
            "Get instant answers with AI-powered analysis"
        )

        # Chat container with enhanced styling
        with styled_group(variant="card"):
            chatbot = styled_chatbot(
                height=CHAT_CONFIG["height"],
                type=CHAT_CONFIG["type"],
                show_copy_button=CHAT_CONFIG["show_copy_button"],
                elem_classes=["main-chatbot"]
            )

            # Loading indicator (initially hidden)
            loading_indicator = create_loading_indicator("Generating response...")

            # Status message container (initially hidden)
            status_message = create_status_message("", "info")

        # Quick actions panel
        quick_actions_panel, quick_buttons, quick_manager = create_quick_actions_panel()

        # Question input section with enhanced styling
        with styled_group(variant="section"):
            create_section_header("Ask Your Question", None)

            with styled_row():
                with styled_column(scale=4):
                    question = styled_textbox(
                        label="Your Question",
                        placeholder="Ask a question about the notes...",
                        lines=2,
                        container_style="chat",
                        elem_classes=["main-question-input"]
                    )

                with styled_column(scale=1):
                    ask_btn = styled_button(
                        text="Ask",
                        variant="primary",
                        elem_classes=["main-ask-btn"]
                    )

        # Action buttons with improved layout
        with styled_group(variant="section"):
            with styled_row():
                clear = styled_button(
                    text="Clear Chat",
                    variant="secondary",
                    icon="🗑️",
                    elem_classes=["clear-btn"]
                )
                new_notes_btn = styled_button(
                    text="New Notes",
                    variant="secondary",
                    icon="📄",
                    elem_classes=["new-notes-btn"]
                )

        # Enhanced options panel
        options_accordion = create_enhanced_options_panel()

        # Setup quick actions event handlers
        quick_manager.setup_event_handlers(question)

    return {
        "chat_phase": chat_phase,
        "question": question,
        "ask_btn": ask_btn,
        "clear": clear,
        "new_notes_btn": new_notes_btn,
        "style": options_accordion["style"],
        "depth": options_accordion["depth"],
        "chatbot": chatbot,
        "loading_indicator": loading_indicator,
        "status_message": status_message,
        "quick_actions_panel": quick_actions_panel,
        "quick_buttons": quick_buttons,
        "quick_manager": quick_manager,
        # Legacy compatibility - keep old button names
        "quick_summary": quick_buttons[0] if len(quick_buttons) > 0 else None,
        "quick_flashcards": quick_buttons[3] if len(quick_buttons) > 3 else None,
        "quick_concepts": quick_buttons[6] if len(quick_buttons) > 6 else None,
        "quick_practice": quick_buttons[4] if len(quick_buttons) > 4 else None,
        "quick_takeaways": quick_buttons[1] if len(quick_buttons) > 1 else None,
    }


def create_enhanced_options_panel() -> Dict[str, any]:
    """Create an enhanced options panel with better styling and organization."""

    with styled_accordion("⚙️ Options & Settings", open=False) as options_accordion:
        with styled_row():
            # Answer Style Options
            with styled_column(scale=2):
                gr.Markdown("**Answer Style**")
                style = gr.CheckboxGroup(
                    choices=OPTIONS_CONFIG["available_styles"],
                    value=OPTIONS_CONFIG["default_style"],
                    label="Select preferred formats",
                    elem_classes=["style-options"]
                )

            # Detail Level
            with styled_column(scale=1):
                gr.Markdown("**Detail Level**")
                depth = gr.Slider(
                    minimum=OPTIONS_CONFIG["depth_range"][0],
                    maximum=OPTIONS_CONFIG["depth_range"][1],
                    value=OPTIONS_CONFIG["default_depth"],
                    step=1,
                    label="Depth (1=Brief, 5=Comprehensive)",
                    elem_classes=["depth-slider"]
                )

        # Advanced options (if enabled)
        if OPTIONS_CONFIG.get("show_advanced_options", False):
            with styled_group(variant="highlight"):
                gr.Markdown("**Advanced Options**")
                gr.Markdown("*More customization options coming soon...*")

    return {
        "accordion": options_accordion,
        "style": style,
        "depth": depth,
    }


def get_chat_phase_css() -> str:
    """Generate CSS styles specific to the chat phase."""
    return """
    /* Chat Phase Specific Styles */

    /* Main chat container */
    .main-chatbot {
        min-height: 400px !important;
        border-radius: var(--radius-lg) !important;
        box-shadow: var(--shadows-md) !important;
        background: white !important;
    }

    /* Question input styling */
    .main-question-input {
        font-size: var(--font-sizes-base) !important;
        border-radius: var(--radius-md) !important;
        border: 2px solid var(--color-gray-200) !important;
        transition: border-color 0.3s ease !important;
    }

    .main-question-input:focus {
        border-color: var(--color-primary) !important;
        box-shadow: 0 0 0 3px var(--color-primary)20 !important;
        outline: none !important;
    }

    /* Ask button styling */
    .main-ask-btn {
        height: 100% !important;
        min-height: 48px !important;
        font-weight: var(--font-weights-semibold) !important;
        border-radius: var(--radius-md) !important;
        transition: all 0.3s ease !important;
    }

    .main-ask-btn:hover {
        transform: translateY(-1px) !important;
        box-shadow: var(--shadows-lg) !important;
    }

    /* Action buttons */
    .clear-btn, .new-notes-btn {
        min-width: 120px !important;
        height: 40px !important;
        border-radius: var(--radius-md) !important;
        transition: all 0.2s ease !important;
    }

    .clear-btn:hover {
        background: var(--color-error)10 !important;
        border-color: var(--color-error)30 !important;
        color: var(--color-error) !important;
    }

    .new-notes-btn:hover {
        background: var(--color-secondary)10 !important;
        border-color: var(--color-secondary)30 !important;
        color: var(--color-secondary) !important;
    }

    /* Options panel styling */
    .style-options {
        display: grid !important;
        grid-template-columns: repeat(auto-fit, minmax(150px, 1fr)) !important;
        gap: var(--spacing-sm) !important;
    }

    .depth-slider {
        margin-top: var(--spacing-md) !important;
    }

    .depth-slider input[type="range"] {
        background: var(--color-primary)30 !important;
        border-radius: var(--radius-full) !important;
    }

    .depth-slider input[type="range"]::-webkit-slider-thumb {
        background: var(--color-primary) !important;
        border-radius: var(--radius-full) !important;
        border: 2px solid white !important;
        box-shadow: var(--shadows-sm) !important;
    }

    /* Enhanced loading states */
    .chatbot-loading {
        position: relative !important;
    }

    .chatbot-loading::after {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: 0 !important;
        right: 0 !important;
        bottom: 0 !important;
        background: rgba(255, 255, 255, 0.8) !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        z-index: 100 !important;
    }

    /* Message bubbles (if using bubble layout) */
    .chatbot .message-bubble-user {
        background: var(--color-primary)10 !important;
        border: 1px solid var(--color-primary)20 !important;
        border-radius: var(--radius-lg) var(--radius-lg) var(--radius-sm) var(--radius-lg) !important;
    }

    .chatbot .message-bubble-assistant {
        background: var(--color-gray-50) !important;
        border: 1px solid var(--color-gray-200) !important;
        border-radius: var(--radius-lg) var(--radius-lg) var(--radius-lg) var(--radius-sm) !important;
    }

    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main-chatbot {
            min-height: 300px !important;
        }

        .main-ask-btn {
            margin-top: var(--spacing-sm) !important;
        }

        .style-options {
            grid-template-columns: 1fr !important;
        }
    }

    /* Accessibility enhancements */
    .main-question-input:focus-visible {
        outline: 2px solid var(--color-primary) !important;
        outline-offset: 2px !important;
    }

    /* Print styles */
    @media print {
        .clear-btn, .new-notes-btn, .main-ask-btn {
            display: none !important;
        }
    }
    """


# Legacy compatibility function
def create_chat_phase_ui():
    """Legacy function name for backward compatibility."""
    return create_enhanced_chat_phase_ui()