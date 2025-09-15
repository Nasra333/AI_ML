"""
Quick Actions component for Study Notes Tab.
Provides categorized quick question buttons with enhanced styling and organization.
"""

import gradio as gr
from typing import List, Dict, Tuple, Callable
from ..styles.components import styled_button, styled_row, styled_group
from ..config.ui_config import QUICK_QUESTIONS_CONFIG

class QuickActionsPanel:
    """Manages the quick actions panel with categorized question buttons."""

    def __init__(self):
        self.buttons: List[gr.Button] = []
        self.button_prompts: Dict[gr.Button, str] = {}

    def create_category_section(self, category_key: str, category_data: Dict) -> List[gr.Button]:
        """
        Create a section for a specific category of quick questions.

        Args:
            category_key: Unique key for the category
            category_data: Category configuration data

        Returns:
            List of button components created for this category
        """
        category_buttons = []

        # Category header with description
        title = category_data.get("title", "Quick Questions")
        description = category_data.get("description", "")

        header_content = f"**{title}**"
        if description:
            header_content += f"\n\n*{description}*"

        gr.Markdown(
            header_content,
            elem_classes=["quick-questions-category-header", f"category-{category_key}"]
        )

        # Create buttons in responsive grid (3 per row on desktop, stacked on mobile)
        questions = category_data.get("questions", [])

        for i in range(0, len(questions), 3):
            row_questions = questions[i:i+3]

            with styled_row(equal_height=True):
                for question in row_questions:
                    btn = self._create_question_button(question, category_key)
                    category_buttons.append(btn)

                # Add empty space for incomplete rows
                for _ in range(3 - len(row_questions)):
                    gr.HTML("", elem_classes=["quick-question-spacer"])

        return category_buttons

    def _create_question_button(self, question: Dict, category_key: str) -> gr.Button:
        """Create a single quick question button with styling and tooltip."""
        btn = styled_button(
            text=question["text"],
            variant="quick",
            icon=question["icon"],
            elem_classes=[
                "quick-question-btn",
                f"category-{category_key}",
                "tooltip-enabled"
            ]
        )

        # Store the prompt for easy access during event handling
        btn._prompt = question["prompt"]
        btn._tooltip = question.get("tooltip", "")
        btn._category = category_key

        self.button_prompts[btn] = question["prompt"]
        self.buttons.append(btn)

        return btn

    def create_panel(self) -> Tuple[gr.Group, List[gr.Button]]:
        """
        Create the compact horizontal quick actions panel.

        Returns:
            Tuple of (panel_group, list_of_buttons)
        """
        with styled_group(variant="compact") as panel:
            # Compact panel header
            gr.Markdown(
                "**⚡ Quick Actions**",
                elem_classes=["quick-actions-compact-header"]
            )

            # Create compact horizontal scrollable container
            gr.HTML('<div class="quick-actions-scroll-container">')

            all_buttons = []

            # Create all buttons in a single horizontal row
            with styled_row():
                # Add primary questions (most commonly used)
                primary_questions = self._get_primary_questions()

                for question_data in primary_questions:
                    btn = self._create_compact_question_button(
                        question_data["question"],
                        question_data["category"]
                    )
                    all_buttons.append(btn)

                # Add "More" dropdown button
                more_btn = self._create_more_button()
                all_buttons.append(more_btn)

            # Store buttons for external access
            self.buttons = all_buttons

            gr.HTML('</div>')  # Close scroll container

        return panel, all_buttons

    def _get_primary_questions(self) -> List[Dict]:
        """Get the most important questions for compact display."""
        primary_questions = []

        # Select 1-2 questions from each category for the main row
        for category_key, category_data in QUICK_QUESTIONS_CONFIG.items():
            questions = category_data.get("questions", [])
            color = category_data.get("color", "#6B7280")

            # Take first 2 questions from each category
            for question in questions[:2]:
                primary_questions.append({
                    "question": question,
                    "category": category_key,
                    "color": color
                })

        return primary_questions

    def _create_compact_question_button(self, question: Dict, category_key: str) -> gr.Button:
        """Create a compact quick question button."""
        btn = styled_button(
            text=question["text"],
            variant="quick",
            icon=question["icon"],
            elem_classes=[
                "quick-question-btn-compact",
                f"category-{category_key}",
                "compact-mode"
            ]
        )

        # Store the prompt for easy access during event handling
        btn._prompt = question["prompt"]
        btn._tooltip = question.get("tooltip", "")
        btn._category = category_key

        self.button_prompts[btn] = question["prompt"]

        return btn

    def _create_more_button(self) -> gr.Button:
        """Create a 'More' dropdown button for additional questions."""
        more_btn = styled_button(
            text="More",
            variant="quick",
            icon="⋯",
            elem_classes=["quick-more-btn", "compact-mode"]
        )

        # This will be handled by a dropdown/modal in the future
        more_btn._prompt = "Show me more study options for these notes."
        self.button_prompts[more_btn] = more_btn._prompt

        return more_btn

    def create_category_based_panel(self) -> Tuple[gr.Group, List[gr.Button]]:
        """
        Create the legacy expanded quick actions panel (for backward compatibility).
        """
        with styled_group(variant="section") as panel:
            # Panel header
            gr.Markdown(
                "## Quick Questions\nGet started quickly with these common study tasks",
                elem_classes=["quick-actions-header"]
            )

            # Create sections for each category
            all_buttons = []
            for category_key, category_data in QUICK_QUESTIONS_CONFIG.items():
                category_buttons = self.create_category_section(category_key, category_data)
                all_buttons.extend(category_buttons)

                # Add spacing between categories (except for the last one)
                if category_key != list(QUICK_QUESTIONS_CONFIG.keys())[-1]:
                    gr.HTML(
                        "<div class='category-separator'></div>",
                        elem_classes=["category-separator"]
                    )

            # Store buttons for external access
            self.buttons = all_buttons

        return panel, all_buttons

    def setup_event_handlers(self, question_textbox: gr.Textbox) -> None:
        """
        Set up event handlers for all quick question buttons.

        Args:
            question_textbox: The textbox to populate with the selected question
        """
        for button in self.buttons:
            if button in self.button_prompts:
                prompt = self.button_prompts[button]
                button.click(
                    lambda p=prompt: p,  # Capture the prompt in closure
                    outputs=[question_textbox],
                    queue=False
                )

    def get_button_by_text(self, text: str) -> gr.Button:
        """Find a button by its text content (for testing/external access)."""
        for button in self.buttons:
            if hasattr(button, '_prompt') and text in str(button.value):
                return button
        return None

    def get_buttons_by_category(self, category_key: str) -> List[gr.Button]:
        """Get all buttons for a specific category."""
        return [btn for btn in self.buttons if hasattr(btn, '_category') and btn._category == category_key]

def create_quick_actions_css() -> str:
    """Generate CSS styles specific to the quick actions panel."""
    return """
    /* Quick Actions Panel Styles */
    .quick-actions-header {
        text-align: center !important;
        margin-bottom: 2rem !important;
        padding-bottom: 1rem !important;
        border-bottom: 2px solid var(--color-gray-200) !important;
    }

    .quick-actions-header h2 {
        color: var(--color-gray-800) !important;
        font-size: var(--font-sizes-xl) !important;
        font-weight: var(--font-weights-bold) !important;
        margin-bottom: 0.5rem !important;
    }

    /* Compact Quick Actions Styles */
    .quick-actions-compact-header {
        margin-bottom: var(--spacing-sm) !important;
        font-size: var(--font-sizes-sm) !important;
        color: var(--color-gray-700) !important;
    }

    .quick-actions-scroll-container {
        display: flex !important;
        overflow-x: auto !important;
        scrollbar-width: none !important; /* Firefox */
        -ms-overflow-style: none !important; /* IE/Edge */
        padding: var(--spacing-xs) 0 !important;
    }

    .quick-actions-scroll-container::-webkit-scrollbar {
        display: none !important; /* Chrome/Safari */
    }

    /* Compact Button Styles */
    .quick-question-btn-compact {
        min-width: 120px !important;
        max-width: 160px !important;
        height: 32px !important;
        padding: var(--spacing-xs) var(--spacing-sm) !important;
        margin-right: var(--spacing-xs) !important;
        font-size: var(--font-sizes-xs) !important;
        white-space: nowrap !important;
        flex-shrink: 0 !important;
        border-radius: var(--radius-full) !important;
        transition: all 0.2s ease !important;
    }

    .quick-question-btn-compact:hover {
        transform: translateY(-1px) !important;
        box-shadow: var(--shadows-sm) !important;
    }

    /* Category Color Coding for Compact Buttons */
    .compact-mode.category-summary {
        background: #EBF8FF !important;
        border-color: #3B82F6 !important;
        color: #1E40AF !important;
    }

    .compact-mode.category-study_tools {
        background: #ECFDF5 !important;
        border-color: #10B981 !important;
        color: #047857 !important;
    }

    .compact-mode.category-analysis {
        background: #F3E8FF !important;
        border-color: #8B5CF6 !important;
        color: #7C3AED !important;
    }

    .quick-more-btn {
        background: var(--color-gray-100) !important;
        border: 1px solid var(--color-gray-300) !important;
        color: var(--color-gray-600) !important;
        min-width: 60px !important;
        flex-shrink: 0 !important;
    }

    .quick-more-btn:hover {
        background: var(--color-gray-200) !important;
        border-color: var(--color-gray-400) !important;
    }

    .quick-questions-category-header {
        margin: 1.5rem 0 1rem 0 !important;
        padding: 0.5rem 0 !important;
    }

    .quick-questions-category-header:first-child {
        margin-top: 0 !important;
    }

    .quick-questions-category-header strong {
        color: var(--color-gray-700) !important;
        font-size: var(--font-sizes-lg) !important;
        font-weight: var(--font-weights-semibold) !important;
        display: flex !important;
        align-items: center !important;
        gap: 0.5rem !important;
    }

    .quick-questions-category-header em {
        color: var(--color-gray-600) !important;
        font-size: var(--font-sizes-sm) !important;
        font-style: normal !important;
        margin-top: 0.25rem !important;
        display: block !important;
    }

    /* Category-specific colors */
    .category-summary .quick-questions-category-header strong {
        border-left: 4px solid #3B82F6 !important;
        padding-left: 0.75rem !important;
    }

    .category-study_tools .quick-questions-category-header strong {
        border-left: 4px solid #10B981 !important;
        padding-left: 0.75rem !important;
    }

    .category-analysis .quick-questions-category-header strong {
        border-left: 4px solid #8B5CF6 !important;
        padding-left: 0.75rem !important;
    }

    /* Button enhancements */
    .quick-question-btn {
        position: relative !important;
        min-height: 48px !important;
        text-align: left !important;
        display: flex !important;
        align-items: center !important;
        justify-content: flex-start !important;
        padding: 0.75rem 1rem !important;
        transition: all 0.3s ease !important;
        border: 2px solid transparent !important;
    }

    .quick-question-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 16px -4px rgba(0, 0, 0, 0.1) !important;
        border-color: var(--color-primary) !important;
    }

    .quick-question-btn:active {
        transform: translateY(0) !important;
    }

    /* Category-specific button hover effects */
    .category-summary .quick-question-btn:hover {
        background: #EBF8FF !important;
        border-color: #3B82F6 !important;
    }

    .category-study_tools .quick-question-btn:hover {
        background: #ECFDF5 !important;
        border-color: #10B981 !important;
    }

    .category-analysis .quick-question-btn:hover {
        background: #F3E8FF !important;
        border-color: #8B5CF6 !important;
    }

    /* Tooltip styles */
    .tooltip-enabled {
        position: relative !important;
    }

    .tooltip-enabled[title]:hover::after {
        content: attr(title) !important;
        position: absolute !important;
        bottom: 100% !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        background: var(--color-gray-900) !important;
        color: white !important;
        padding: 0.5rem 0.75rem !important;
        border-radius: var(--radius-md) !important;
        font-size: var(--font-sizes-sm) !important;
        white-space: nowrap !important;
        z-index: 1000 !important;
        box-shadow: var(--shadows-lg) !important;
        margin-bottom: 0.5rem !important;
    }

    .tooltip-enabled[title]:hover::before {
        content: '' !important;
        position: absolute !important;
        bottom: 100% !important;
        left: 50% !important;
        transform: translateX(-50%) !important;
        border: 5px solid transparent !important;
        border-top-color: var(--color-gray-900) !important;
        z-index: 1001 !important;
    }

    /* Category separators */
    .category-separator {
        height: 1px !important;
        background: linear-gradient(
            to right,
            transparent,
            var(--color-gray-300),
            transparent
        ) !important;
        margin: 2rem 0 !important;
    }

    /* Spacer elements */
    .quick-question-spacer {
        flex: 1 !important;
        min-width: 0 !important;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .quick-actions-header h2 {
            font-size: var(--font-sizes-lg) !important;
        }

        .quick-question-btn {
            width: 100% !important;
            margin-bottom: 0.5rem !important;
            min-height: 56px !important;
        }

        .category-separator {
            margin: 1.5rem 0 !important;
        }

        /* Hide tooltips on mobile */
        .tooltip-enabled[title]:hover::after,
        .tooltip-enabled[title]:hover::before {
            display: none !important;
        }
    }

    /* Animation improvements */
    @media (prefers-reduced-motion: no-preference) {
        .quick-question-btn {
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        .quick-question-btn:hover {
            animation: subtle-pulse 2s infinite !important;
        }
    }

    @keyframes subtle-pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.9; }
    }

    /* High contrast mode support */
    @media (prefers-contrast: high) {
        .quick-question-btn {
            border: 2px solid var(--color-gray-800) !important;
        }

        .quick-question-btn:hover {
            background: var(--color-gray-100) !important;
            border-color: var(--color-gray-900) !important;
        }
    }
    """

# Convenience function for external use
def create_quick_actions_panel() -> Tuple[gr.Group, List[gr.Button], QuickActionsPanel]:
    """
    Create a complete compact quick actions panel with all functionality.

    Returns:
        Tuple of (panel_component, button_list, panel_manager)
    """
    panel_manager = QuickActionsPanel()
    panel_component, button_list = panel_manager.create_panel()
    return panel_component, button_list, panel_manager

# Legacy function for backward compatibility
def create_quick_actions_panel_legacy() -> Tuple[gr.Group, List[gr.Button], QuickActionsPanel]:
    """
    Create the old expanded quick actions panel for backward compatibility.
    """
    panel_manager = QuickActionsPanel()
    panel_component, button_list = panel_manager.create_category_based_panel()
    return panel_component, button_list, panel_manager