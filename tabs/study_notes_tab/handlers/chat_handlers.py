"""
Chat handling logic for study notes tab.
Manages Q&A functionality, prompt building, and AI interaction.
"""
import gradio as gr
from utils import onSystemPromptChanged, userMessage
from constants import default_system_prompts


def build_qna_prompt(notes_content: str, question: str, style_opts: list, depth_val: int) -> str:
    """
    Build a Q&A prompt for the AI model.

    Args:
        notes_content: Study notes content
        question: User's question
        style_opts: Answer style preferences
        depth_val: Detail level (1-5)

    Returns:
        Formatted prompt string
    """
    question = (question or "").strip()
    style_txt = ", ".join(style_opts or []) or "Bullet Points"

    return (
        "Using the student's study notes below, answer the question. "
        "Cite key concepts from the notes, avoid fabricating content, and keep it well-structured. "
        f"Prefer style: {style_txt}. Detail level: {depth_val}.\n\n"
        f"Study Notes:\n{notes_content}\n\nQuestion:\n{question}"
    )


def handle_question_clean_ui(notes_content: str, question: str, style_opts: list, depth_val: int, history: list):
    """
    Handle user question with clean UI that shows only the question in chat.
    This function prepares the display history and sets up the AI context.

    Args:
        notes_content: Processed study notes
        question: User's question
        style_opts: Answer style preferences
        depth_val: Detail level
        history: Chat history

    Returns:
        Tuple of (cleared_question, updated_display_history)
    """
    if not notes_content:
        gr.Warning("No study notes available. Please process notes first.")
        return question, history

    if not validate_question(question):
        gr.Warning("Please enter a question.")
        return question, history

    # Set system prompt for study notes Q&A
    onSystemPromptChanged(
        default_system_prompts.get("Study Notes Question And Answer", "Study Notes Question And Answer")
    )

    # Add only the clean user question to chat history for display
    clean_question = question.strip()
    updated_history = history + [{"role": "user", "content": clean_question}]

    # Store the full context for AI processing in a global variable or state
    # This is a bit of a hack but necessary for the Gradio event chain
    global _current_ai_context
    _current_ai_context = build_qna_prompt(notes_content, question, style_opts, depth_val)

    return "", updated_history


def get_ai_response_with_context(display_history: list):
    """
    Generate AI response using the stored context while maintaining clean display history.
    This function is called in the .then() chain after handle_question_clean_ui.

    Args:
        display_history: Clean chat history for display

    Yields:
        Updated display history with AI response
    """
    global _current_ai_context

    if not _current_ai_context:
        return display_history

    # Import here to avoid circular imports
    from utils import responseStream

    # Create AI processing history with full context
    # Use only the system message and the full context prompt
    ai_history = []
    if display_history:
        # Add all previous messages except the last user message
        ai_history = display_history[:-1]

    # Add the full context as the current user message for AI processing
    ai_processing_history = ai_history + [{"role": "user", "content": _current_ai_context}]

    # Get the AI response
    for updated_ai_history in responseStream(ai_processing_history):
        # Take the AI response and add it to our clean display history
        if updated_ai_history and len(updated_ai_history) > len(ai_history):
            ai_response = updated_ai_history[-1]  # Get the latest AI response
            if ai_response.get("role") == "assistant":
                # Update the display history with the AI response
                yield display_history + [ai_response]

    # Clean up the context
    _current_ai_context = None


# Global variable to store AI context (not ideal but works with Gradio's event system)
_current_ai_context = None


# Keep the original function for backward compatibility if needed
def handle_question(notes_content: str, question: str, style_opts: list, depth_val: int, history: list):
    """
    Original handle_question function - kept for backward compatibility.
    Use handle_question_clean_ui for clean UI experience.
    """
    if not notes_content:
        gr.Warning("No study notes available. Please process notes first.")
        return question, history

    # Set system prompt for study notes Q&A
    onSystemPromptChanged(
        default_system_prompts.get("Study Notes Question And Answer", "Study Notes Question And Answer")
    )

    # Build and send prompt (shows full prompt in chat)
    prompt = build_qna_prompt(notes_content, question, style_opts, depth_val)
    from utils import userMessage
    return userMessage(prompt, history)


def validate_question(question: str) -> bool:
    """
    Validate that question is not empty.

    Args:
        question: Question text to validate

    Returns:
        True if question is valid, False otherwise
    """
    return bool(question and question.strip())