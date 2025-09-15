"""
Enhanced input phase UI components for study notes tab.
Features improved styling, better file handling, and enhanced UX.
"""
import gradio as gr
from typing import Dict, List
from ..styles.components import (
    styled_textbox, styled_button, styled_row, styled_column,
    styled_group, create_section_header, create_loading_indicator,
    create_status_message
)
from ..utils.file_readers import get_supported_file_types
from ..config.ui_config import INPUT_PHASE_CONFIG


def create_enhanced_input_phase_ui() -> Dict[str, any]:
    """
    Create the enhanced input phase UI with improved styling and features.
    This function should be called within a Gradio context.

    Returns:
        Dictionary containing all input phase components
    """
    # Create main input phase container
    input_phase = styled_group(variant="default", visible=True)

    with input_phase:
        # Enhanced section header
        create_section_header(
            "Study Notes Input",
            "Choose how you'd like to provide your study materials"
        )

        # Input method selection with enhanced styling
        with styled_group(variant="card"):
            gr.Markdown("**Step 1: Select Input Method**")

            input_method = gr.Radio(
                choices=["Paste Notes", "Upload File"],
                value="Paste Notes",
                label="How would you like to provide your notes?",
                elem_classes=["input-method-radio"],
                info="Choose between typing/pasting text or uploading a document file"
            )

        # Enhanced input sections
        with styled_group(variant="section"):
            # Paste input section
            paste_input = styled_group(variant="highlight", visible=True)
            with paste_input:
                gr.Markdown("**✍️ Text Input**")
                notes_textbox = styled_textbox(
                    label="Study Notes",
                    placeholder="Paste or type your study notes here...\n\nTip: You can paste from PDFs, web pages, or type directly.",
                    lines=INPUT_PHASE_CONFIG["textbox_lines"],
                    container_style="input_phase",
                    elem_classes=["notes-textbox"]
                )

                # Character counter and tips
                gr.HTML(
                    """
                    <div class="input-tips">
                        <div class="tip-item">💡 <strong>Pro tip:</strong> The AI works best with structured notes</div>
                        <div class="tip-item">📋 <strong>Formats:</strong> Bullet points, headings, and numbered lists are ideal</div>
                        <div class="tip-item">⚡ <strong>Length:</strong> No strict limit, but very long texts may take longer to process</div>
                    </div>
                    """,
                    elem_classes=["input-tips-container"]
                )

            # File upload section
            file_input = styled_group(variant="highlight", visible=False)
            with file_input:
                gr.Markdown("**📁 File Upload**")

                # File upload with enhanced styling
                file_upload = gr.File(
                    label="Upload Study Notes",
                    file_types=get_supported_file_types(),
                    type="filepath",
                    elem_classes=["file-upload"],
                    file_count="single"
                )

                # Supported formats info
                supported_formats = ", ".join(get_supported_file_types())
                gr.Markdown(
                    f"**Supported formats:** {supported_formats}\n\n"
                    f"**Maximum file size:** {INPUT_PHASE_CONFIG['max_file_size']}",
                    elem_classes=["file-info"]
                )

                # File preview area (initially hidden)
                file_preview = gr.HTML(
                    "",
                    visible=False,
                    elem_classes=["file-preview"]
                )

        # Processing section
        with styled_group(variant="section"):
            gr.Markdown("**Step 2: Process Your Notes**")

            with styled_row():
                with styled_column(scale=3):
                    gr.Markdown("*Ready to analyze your study materials? Click the button below to get started.*")

                with styled_column(scale=1):
                    process_btn = styled_button(
                        text="Process Notes",
                        variant="primary",
                        icon="🚀",
                        elem_classes=["process-notes-btn"],
                        size="lg"
                    )

            # Processing status indicators
            processing_indicator = create_loading_indicator("Processing your notes...")
            processing_status = create_status_message("", "info")

        # Help section
        create_help_section()

    return {
        "input_phase": input_phase,
        "input_method": input_method,
        "paste_input": paste_input,
        "file_input": file_input,
        "notes_textbox": notes_textbox,
        "file_upload": file_upload,
        "file_preview": file_preview,
        "process_btn": process_btn,
        "processing_indicator": processing_indicator,
        "processing_status": processing_status,
    }


def create_help_section():
    """Create a collapsible help section with usage tips."""
    with gr.Accordion("❓ Need Help? Click here for tips", open=False, elem_classes=["help-accordion"]):
        gr.Markdown("""
        ### 📚 How to Get the Best Results

        **For Text Input:**
        - Copy and paste from your textbooks, PDFs, or class notes
        - Use clear headings and bullet points when possible
        - Include all relevant information you want to study from

        **For File Upload:**
        - Supported formats: PDF, Word documents, plain text, and Markdown files
        - Make sure your files contain readable text (not just images)
        - Files should be well-formatted for best results

        **Study Tips:**
        - Break large documents into smaller, focused sections for better analysis
        - Include definitions, examples, and key concepts
        - The AI can work with any subject: science, history, literature, business, etc.

        ### 🔧 Troubleshooting

        **If processing fails:**
        - Check that your file isn't corrupted or password-protected
        - Try with a smaller file or shorter text
        - Make sure the content is in a supported language

        **For better results:**
        - Provide context about what subject you're studying
        - Include any specific areas you want to focus on
        - Use the quick questions to guide your study session
        """, elem_classes=["help-content"])


def get_input_phase_css() -> str:
    """Generate CSS styles specific to the input phase."""
    return """
    /* Input Phase Specific Styles */

    /* Input method radio styling */
    .input-method-radio {
        background: white !important;
        border: 1px solid var(--color-gray-200) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--spacing-lg) !important;
    }

    .input-method-radio label {
        font-weight: var(--font-weights-medium) !important;
        margin-bottom: var(--spacing-sm) !important;
    }

    /* Notes textbox styling */
    .notes-textbox {
        font-family: 'SF Mono', 'Monaco', 'Cascadia Code', 'Roboto Mono', monospace !important;
        font-size: var(--font-sizes-sm) !important;
        line-height: var(--line-heights-relaxed) !important;
        border: 2px dashed var(--color-gray-300) !important;
        border-radius: var(--radius-lg) !important;
        background: var(--color-gray-50) !important;
        transition: all 0.3s ease !important;
    }

    .notes-textbox:focus {
        border-color: var(--color-primary) !important;
        border-style: solid !important;
        background: white !important;
        box-shadow: 0 0 0 3px var(--color-primary)20 !important;
    }

    /* Input tips styling */
    .input-tips-container {
        margin-top: var(--spacing-md) !important;
    }

    .input-tips {
        background: var(--color-info)10 !important;
        border: 1px solid var(--color-info)30 !important;
        border-radius: var(--radius-md) !important;
        padding: var(--spacing-md) !important;
    }

    .tip-item {
        display: flex !important;
        align-items: flex-start !important;
        gap: var(--spacing-sm) !important;
        margin-bottom: var(--spacing-sm) !important;
        font-size: var(--font-sizes-sm) !important;
        color: var(--color-gray-700) !important;
        line-height: var(--line-heights-normal) !important;
    }

    .tip-item:last-child {
        margin-bottom: 0 !important;
    }

    .tip-item strong {
        color: var(--color-info) !important;
    }

    /* File upload styling */
    .file-upload {
        border: 2px dashed var(--color-primary)40 !important;
        border-radius: var(--radius-lg) !important;
        background: var(--color-primary)05 !important;
        padding: var(--spacing-xl) !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
    }

    .file-upload:hover {
        border-color: var(--color-primary) !important;
        background: var(--color-primary)10 !important;
        transform: translateY(-2px) !important;
        box-shadow: var(--shadows-lg) !important;
    }

    .file-upload.drag-active {
        border-color: var(--color-success) !important;
        background: var(--color-success)10 !important;
    }

    /* File info styling */
    .file-info {
        background: var(--color-gray-50) !important;
        border: 1px solid var(--color-gray-200) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--spacing-md) !important;
        margin-top: var(--spacing-md) !important;
        font-size: var(--font-sizes-sm) !important;
    }

    /* File preview styling */
    .file-preview {
        background: white !important;
        border: 1px solid var(--color-gray-200) !important;
        border-radius: var(--radius-md) !important;
        padding: var(--spacing-md) !important;
        margin-top: var(--spacing-md) !important;
        max-height: 200px !important;
        overflow-y: auto !important;
    }

    /* Process button styling */
    .process-notes-btn {
        min-width: 150px !important;
        min-height: 48px !important;
        font-size: var(--font-sizes-lg) !important;
        font-weight: var(--font-weights-bold) !important;
        border-radius: var(--radius-lg) !important;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1) !important;
        position: relative !important;
        overflow: hidden !important;
    }

    .process-notes-btn:hover {
        transform: translateY(-2px) !important;
        box-shadow: var(--shadows-lg) !important;
    }

    .process-notes-btn:active {
        transform: translateY(0) !important;
    }

    /* Processing states */
    .process-notes-btn.processing {
        pointer-events: none !important;
        opacity: 0.7 !important;
    }

    .process-notes-btn.processing::after {
        content: '' !important;
        position: absolute !important;
        top: 0 !important;
        left: -100% !important;
        width: 100% !important;
        height: 100% !important;
        background: linear-gradient(
            90deg,
            transparent,
            rgba(255, 255, 255, 0.4),
            transparent
        ) !important;
        animation: shimmer 1.5s infinite !important;
    }

    @keyframes shimmer {
        0% { left: -100%; }
        100% { left: 100%; }
    }

    /* Help section styling */
    .help-accordion {
        margin-top: var(--spacing-xl) !important;
        background: var(--color-gray-50) !important;
        border: 1px solid var(--color-gray-200) !important;
        border-radius: var(--radius-md) !important;
    }

    .help-content {
        padding: var(--spacing-md) !important;
        line-height: var(--line-heights-relaxed) !important;
    }

    .help-content h3 {
        color: var(--color-primary) !important;
        font-size: var(--font-sizes-lg) !important;
        font-weight: var(--font-weights-semibold) !important;
        margin-top: var(--spacing-xl) !important;
        margin-bottom: var(--spacing-md) !important;
        border-bottom: 2px solid var(--color-primary)30 !important;
        padding-bottom: var(--spacing-sm) !important;
    }

    .help-content h3:first-child {
        margin-top: 0 !important;
    }

    .help-content strong {
        color: var(--color-gray-800) !important;
        font-weight: var(--font-weights-semibold) !important;
    }

    .help-content ul {
        margin-left: var(--spacing-lg) !important;
    }

    .help-content li {
        margin-bottom: var(--spacing-sm) !important;
        color: var(--color-gray-700) !important;
    }

    /* Responsive design */
    @media (max-width: 768px) {
        .notes-textbox {
            font-size: var(--font-sizes-base) !important;
        }

        .input-tips {
            padding: var(--spacing-sm) !important;
        }

        .tip-item {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: var(--spacing-xs) !important;
        }

        .process-notes-btn {
            width: 100% !important;
            margin-top: var(--spacing-md) !important;
        }

        .file-upload {
            padding: var(--spacing-md) !important;
        }
    }

    /* Accessibility enhancements */
    .process-notes-btn:focus-visible {
        outline: 2px solid var(--color-primary) !important;
        outline-offset: 2px !important;
    }

    .notes-textbox:focus-visible {
        outline: 2px solid var(--color-primary) !important;
        outline-offset: 2px !important;
    }

    /* Dark mode support (future) */
    @media (prefers-color-scheme: dark) {
        .notes-textbox {
            background: var(--color-gray-800) !important;
            color: var(--color-gray-100) !important;
            border-color: var(--color-gray-600) !important;
        }

        .input-tips {
            background: var(--color-info)20 !important;
            border-color: var(--color-info)40 !important;
        }
    }
    """


# Legacy compatibility function
def create_input_phase_ui():
    """Legacy function name for backward compatibility."""
    return create_enhanced_input_phase_ui()