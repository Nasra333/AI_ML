"""
Reusable Gradio component builders with consistent styling.
Provides pre-styled components following the design system.
"""

import gradio as gr
from typing import List, Dict, Optional, Any
from .theme import *

def styled_button(
    text: str,
    variant: str = "secondary",
    size: str = "md",
    icon: Optional[str] = None,
    **kwargs
) -> gr.Button:
    """
    Create a styled button with consistent theming.

    Args:
        text: Button text
        variant: "primary", "secondary", "quick" (for quick question buttons)
        size: "sm", "md", "lg"
        icon: Optional emoji or icon to prepend
        **kwargs: Additional Gradio button arguments
    """
    display_text = f"{icon} {text}" if icon else text

    # Apply styling based on variant
    if variant == "primary":
        kwargs.setdefault("variant", "primary")
        kwargs.setdefault("elem_classes", []).append("styled-primary-btn")
    elif variant == "quick":
        kwargs.setdefault("size", "sm")
        kwargs.setdefault("elem_classes", []).append("styled-quick-btn")
    else:  # secondary
        kwargs.setdefault("elem_classes", []).append("styled-secondary-btn")

    return gr.Button(display_text, **kwargs)

def styled_textbox(
    label: str,
    placeholder: str = "",
    lines: int = 1,
    container_style: str = "default",
    **kwargs
) -> gr.Textbox:
    """
    Create a styled textbox with consistent theming.

    Args:
        label: Textbox label
        placeholder: Placeholder text
        lines: Number of lines for multiline input
        container_style: "default", "chat", "input_phase"
        **kwargs: Additional Gradio textbox arguments
    """
    classes = kwargs.setdefault("elem_classes", [])
    classes.append("styled-textbox")

    if container_style == "chat":
        classes.append("chat-textbox")
    elif container_style == "input_phase":
        classes.append("input-phase-textbox")

    return gr.Textbox(
        label=label,
        placeholder=placeholder,
        lines=lines,
        **kwargs
    )

def styled_chatbot(**kwargs) -> gr.Chatbot:
    """Create a styled chatbot with enhanced appearance."""
    classes = kwargs.setdefault("elem_classes", [])
    classes.append("styled-chatbot")

    kwargs.setdefault("type", "messages")
    kwargs.setdefault("height", 400)

    return gr.Chatbot(**kwargs)

def styled_accordion(
    label: str,
    open: bool = False,
    **kwargs
) -> gr.Accordion:
    """Create a styled accordion with consistent theming."""
    classes = kwargs.setdefault("elem_classes", [])
    classes.append("styled-accordion")

    return gr.Accordion(label, open=open, **kwargs)

def styled_row(equal_height: bool = False, **kwargs) -> gr.Row:
    """Create a styled row with optional equal height."""
    classes = kwargs.setdefault("elem_classes", [])
    classes.append("styled-row")

    if equal_height:
        classes.append("equal-height")

    return gr.Row(**kwargs)

def styled_column(
    variant: str = "default",
    scale: Optional[int] = None,
    **kwargs
) -> gr.Column:
    """
    Create a styled column with consistent theming.

    Args:
        variant: "default", "sidebar", "main", "card"
        scale: Column scale for relative sizing
        **kwargs: Additional Gradio column arguments
    """
    classes = kwargs.setdefault("elem_classes", [])
    classes.append(f"styled-column-{variant}")

    if scale:
        kwargs["scale"] = scale

    return gr.Column(**kwargs)

def styled_group(
    variant: str = "default",
    visible: bool = True,
    **kwargs
) -> gr.Group:
    """
    Create a styled group container.

    Args:
        variant: "default", "card", "section", "highlight"
        visible: Initial visibility state
        **kwargs: Additional Gradio group arguments
    """
    classes = kwargs.setdefault("elem_classes", [])
    classes.append(f"styled-group-{variant}")

    return gr.Group(visible=visible, **kwargs)

def create_quick_question_grid(questions_config: Dict) -> List[gr.Button]:
    """
    Create a grid of quick question buttons organized by category.

    Args:
        questions_config: Configuration dict with categories and questions

    Returns:
        List of button components for event binding
    """
    buttons = []

    for category_key, category_data in questions_config.items():
        # Create category header
        gr.Markdown(
            f"**{category_data['title']}**",
            elem_classes=["quick-questions-category-header"]
        )

        # Create buttons in rows of 3
        questions = category_data["questions"]
        for i in range(0, len(questions), 3):
            row_questions = questions[i:i+3]

            with styled_row():
                for question in row_questions:
                    btn = styled_button(
                        text=question["text"],
                        variant="quick",
                        icon=question["icon"],
                        elem_classes=["quick-question-btn"]
                    )
                    # Store prompt in a custom attribute for easy access
                    btn._prompt = question["prompt"]
                    buttons.append(btn)

                # Fill remaining slots if needed
                for _ in range(3 - len(row_questions)):
                    gr.HTML("")  # Empty space

    return buttons

def create_section_header(title: str, subtitle: Optional[str] = None) -> None:
    """Create a styled section header with optional subtitle."""
    header_md = f"## {title}"
    if subtitle:
        header_md += f"\n{subtitle}"

    gr.Markdown(header_md, elem_classes=["section-header"])

def create_loading_indicator(text: str = "Processing...") -> gr.HTML:
    """Create a loading indicator component."""
    loading_html = f"""
    <div class="loading-indicator">
        <div class="spinner"></div>
        <span>{text}</span>
    </div>
    """
    return gr.HTML(loading_html, visible=False, elem_classes=["loading-container"])

def create_status_message(
    message: str,
    status: str = "info",
    dismissible: bool = True
) -> gr.HTML:
    """
    Create a status message component.

    Args:
        message: Message text
        status: "success", "error", "warning", "info"
        dismissible: Whether the message can be dismissed
    """
    dismiss_btn = """
        <button class="status-dismiss" onclick="this.parentElement.style.display='none'">×</button>
    """ if dismissible else ""

    status_html = f"""
    <div class="status-message status-{status}">
        <span class="status-icon"></span>
        <span class="status-text">{message}</span>
        {dismiss_btn}
    </div>
    """
    return gr.HTML(status_html, visible=False, elem_classes=["status-container"])

def get_component_css() -> str:
    """Generate CSS styles for all styled components."""
    return f"""
    {get_css_variables()}

    /* Base component styles */
    .styled-primary-btn {{
        {PRIMARY_BUTTON_STYLE}
    }}

    .styled-secondary-btn {{
        {SECONDARY_BUTTON_STYLE}
    }}

    .styled-quick-btn {{
        {QUICK_BUTTON_STYLE}
    }}

    .styled-quick-btn:hover {{
        {QUICK_BUTTON_HOVER}
    }}

    .styled-chatbot {{
        {CHAT_CONTAINER_STYLE}
    }}

    .styled-textbox {{
        border-radius: {RADIUS['md']} !important;
        border-color: {COLORS['gray_300']} !important;
    }}

    .styled-accordion {{
        background: {COLORS['gray_50']} !important;
        border: 1px solid {COLORS['gray_200']} !important;
        border-radius: {RADIUS['md']} !important;
        margin: {SPACING['md']} 0 !important;
    }}

    .styled-row {{
        gap: {SPACING['md']} !important;
        align-items: flex-start !important;
    }}

    .styled-row.equal-height {{
        align-items: stretch !important;
    }}

    .styled-column-card {{
        background: white !important;
        border: 1px solid {COLORS['gray_200']} !important;
        border-radius: {RADIUS['lg']} !important;
        padding: {SPACING['lg']} !important;
        box-shadow: {SHADOWS['sm']} !important;
    }}

    .styled-group-card {{
        background: white !important;
        border: 1px solid {COLORS['gray_200']} !important;
        border-radius: {RADIUS['lg']} !important;
        padding: {SPACING['lg']} !important;
        margin: {SPACING['md']} 0 !important;
    }}

    .styled-group-section {{
        background: {COLORS['gray_50']} !important;
        border-radius: {RADIUS['md']} !important;
        padding: {SPACING['lg']} !important;
        margin: {SPACING['md']} 0 !important;
    }}

    .styled-group-highlight {{
        background: {COLORS['primary']}10 !important;
        border: 1px solid {COLORS['primary']}30 !important;
        border-radius: {RADIUS['md']} !important;
        padding: {SPACING['lg']} !important;
        margin: {SPACING['md']} 0 !important;
    }}

    .styled-group-compact {{
        background: white !important;
        border: 1px solid {COLORS['gray_200']} !important;
        border-radius: {RADIUS['md']} !important;
        padding: {SPACING['sm']} {SPACING['md']} !important;
        margin: {SPACING['sm']} 0 !important;
    }}

    /* Quick questions specific styles */
    .quick-questions-category-header {{
        color: {COLORS['gray_700']} !important;
        font-size: {TYPOGRAPHY['font_sizes']['sm']} !important;
        font-weight: {TYPOGRAPHY['font_weights']['semibold']} !important;
        margin: {SPACING['lg']} 0 {SPACING['sm']} 0 !important;
        text-transform: uppercase !important;
        letter-spacing: 0.05em !important;
    }}

    .quick-questions-category-header:first-child {{
        margin-top: 0 !important;
    }}

    .quick-question-btn {{
        min-height: 40px !important;
        text-align: left !important;
    }}

    /* Section headers */
    .section-header h2 {{
        {SECTION_HEADER_STYLE}
        border-bottom: 2px solid {COLORS['primary']} !important;
        padding-bottom: {SPACING['sm']} !important;
    }}

    /* Loading indicator */
    .loading-container {{
        text-align: center !important;
        padding: {SPACING['xl']} !important;
    }}

    .loading-indicator {{
        display: inline-flex !important;
        align-items: center !important;
        gap: {SPACING['sm']} !important;
        color: {COLORS['gray_600']} !important;
    }}

    .spinner {{
        width: 16px !important;
        height: 16px !important;
        border: 2px solid {COLORS['gray_300']} !important;
        border-top: 2px solid {COLORS['primary']} !important;
        border-radius: 50% !important;
        animation: spin 1s linear infinite !important;
    }}

    @keyframes spin {{
        0% {{ transform: rotate(0deg); }}
        100% {{ transform: rotate(360deg); }}
    }}

    /* Status messages */
    .status-message {{
        display: flex !important;
        align-items: center !important;
        gap: {SPACING['sm']} !important;
        padding: {SPACING['md']} !important;
        border-radius: {RADIUS['md']} !important;
        margin: {SPACING['sm']} 0 !important;
        position: relative !important;
    }}

    .status-success {{
        background: {COLORS['success']}15 !important;
        border: 1px solid {COLORS['success']}30 !important;
        color: {COLORS['success']} !important;
    }}

    .status-error {{
        background: {COLORS['error']}15 !important;
        border: 1px solid {COLORS['error']}30 !important;
        color: {COLORS['error']} !important;
    }}

    .status-warning {{
        background: {COLORS['warning']}15 !important;
        border: 1px solid {COLORS['warning']}30 !important;
        color: {COLORS['warning']} !important;
    }}

    .status-info {{
        background: {COLORS['info']}15 !important;
        border: 1px solid {COLORS['info']}30 !important;
        color: {COLORS['info']} !important;
    }}

    .status-dismiss {{
        position: absolute !important;
        right: {SPACING['sm']} !important;
        top: 50% !important;
        transform: translateY(-50%) !important;
        background: none !important;
        border: none !important;
        font-size: 18px !important;
        cursor: pointer !important;
        opacity: 0.7 !important;
        transition: opacity 0.2s !important;
    }}

    .status-dismiss:hover {{
        opacity: 1 !important;
    }}

    /* Responsive design */
    @media (max-width: 768px) {{
        .styled-row {{
            flex-direction: column !important;
        }}

        .quick-question-btn {{
            width: 100% !important;
            margin-bottom: {SPACING['sm']} !important;
        }}

        .styled-group-card,
        .styled-group-section {{
            padding: {SPACING['md']} !important;
        }}
    }}
    """