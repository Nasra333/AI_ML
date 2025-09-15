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


def handle_question(notes_content: str, question: str, style_opts: list, depth_val: int, history: list):
    """
    Handle user question and generate AI response.

    Args:
        notes_content: Processed study notes
        question: User's question
        style_opts: Answer style preferences
        depth_val: Detail level
        history: Chat history

    Returns:
        Tuple of (cleared_question, updated_history)
    """
    if not notes_content:
        gr.Warning("No study notes available. Please process notes first.")
        return question, history

    # Set system prompt for study notes Q&A
    onSystemPromptChanged(
        default_system_prompts.get("Study Notes Question And Answer", "Study Notes Question And Answer")
    )

    # Build and send prompt
    prompt = build_qna_prompt(notes_content, question, style_opts, depth_val)
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