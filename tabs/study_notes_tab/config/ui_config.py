"""
UI configuration settings for the Study Notes Tab.
Centralizes all UI-related settings for easy customization.
"""

from typing import Dict, List, Any

# Chat Configuration
CHAT_CONFIG = {
    "height": 400,
    "type": "messages",
    "show_copy_button": True,
    "show_share_button": False,
    "bubble_full_width": False,
    "layout": "bubble",  # or "panel"
}

# Input Phase Configuration
INPUT_PHASE_CONFIG = {
    "textbox_lines": 10,
    "textbox_max_lines": 20,
    "file_upload_types": [".txt", ".md", ".pdf", ".docx"],
    "max_file_size": "10MB",
    "show_file_preview": True,
}

# Options Configuration
OPTIONS_CONFIG = {
    "default_style": ["Bullet Points"],
    "available_styles": [
        "Bullet Points",
        "Numbered",
        "Flashcards",
        "Short Paragraphs",
        "Outline",
        "Q&A"
    ],
    "default_depth": 3,
    "depth_range": (1, 5),
    "show_advanced_options": True,
}

# Quick Questions Configuration (Enhanced)
QUICK_QUESTIONS_CONFIG = {
    "summary": {
        "title": "📋 Summary & Overview",
        "description": "Get comprehensive overviews and key points",
        "color": "#3B82F6",  # Blue
        "questions": [
            {
                "icon": "📝",
                "text": "Summarize main points",
                "prompt": "Summarize the main points from my study notes.",
                "tooltip": "Get a concise summary of the most important information"
            },
            {
                "icon": "🎯",
                "text": "Key takeaways",
                "prompt": "What are the most important takeaways from my study notes?",
                "tooltip": "Focus on the essential lessons and insights"
            },
            {
                "icon": "🔍",
                "text": "Overview",
                "prompt": "Give me a comprehensive overview of my study notes.",
                "tooltip": "Get a complete picture of all topics covered"
            },
        ]
    },
    "study_tools": {
        "title": "🎓 Study Tools",
        "description": "Create materials to enhance your learning",
        "color": "#10B981",  # Green
        "questions": [
            {
                "icon": "🃏",
                "text": "Create flashcards",
                "prompt": "Create flashcards from the key concepts in my notes.",
                "tooltip": "Generate flashcards for active recall practice"
            },
            {
                "icon": "❓",
                "text": "Practice questions",
                "prompt": "Generate practice questions based on my study notes.",
                "tooltip": "Create questions to test your understanding"
            },
            {
                "icon": "📊",
                "text": "Quiz me",
                "prompt": "Create a quiz to test my understanding of these notes.",
                "tooltip": "Interactive quiz with immediate feedback"
            },
        ]
    },
    "analysis": {
        "title": "💡 Analysis & Understanding",
        "description": "Deepen your comprehension of the material",
        "color": "#8B5CF6",  # Purple
        "questions": [
            {
                "icon": "💡",
                "text": "Explain concepts",
                "prompt": "Explain the key concepts from my study notes in simple terms.",
                "tooltip": "Break down complex ideas into understandable explanations"
            },
            {
                "icon": "🔗",
                "text": "Find connections",
                "prompt": "What are the connections between different concepts in my notes?",
                "tooltip": "Discover relationships and patterns in the material"
            },
            {
                "icon": "🤔",
                "text": "Clarify topics",
                "prompt": "Help me clarify any confusing topics from my notes.",
                "tooltip": "Get help with difficult or unclear concepts"
            },
        ]
    }
}

# Layout Configuration
LAYOUT_CONFIG = {
    "container_max_width": "1200px",
    "sidebar_width": "300px",
    "main_content_padding": "24px",
    "mobile_breakpoint": "768px",
    "use_responsive_design": True,
}

# Animation Configuration
ANIMATION_CONFIG = {
    "enable_animations": True,
    "transition_duration": "0.2s",
    "hover_effects": True,
    "loading_animations": True,
}

# Accessibility Configuration
ACCESSIBILITY_CONFIG = {
    "high_contrast_mode": False,
    "show_tooltips": True,
    "keyboard_navigation": True,
    "screen_reader_support": True,
    "focus_indicators": True,
}

# Feature Flags
FEATURE_FLAGS = {
    "enable_dark_mode": False,
    "enable_advanced_options": True,
    "enable_file_drag_drop": True,
    "enable_keyboard_shortcuts": True,
    "enable_auto_save": False,
    "enable_undo_redo": False,  # Future feature
    "enable_export_options": False,  # Future feature
}

# Custom CSS Classes (for advanced users)
CUSTOM_CSS_CLASSES = {
    "main_container": "study-notes-main-container",
    "input_phase": "study-notes-input-phase",
    "chat_phase": "study-notes-chat-phase",
    "quick_questions": "study-notes-quick-questions",
    "options_panel": "study-notes-options-panel",
}

def get_ui_config() -> Dict[str, Any]:
    """Get the complete UI configuration as a single dictionary."""
    return {
        "chat": CHAT_CONFIG,
        "input_phase": INPUT_PHASE_CONFIG,
        "options": OPTIONS_CONFIG,
        "quick_questions": QUICK_QUESTIONS_CONFIG,
        "layout": LAYOUT_CONFIG,
        "animation": ANIMATION_CONFIG,
        "accessibility": ACCESSIBILITY_CONFIG,
        "features": FEATURE_FLAGS,
        "css_classes": CUSTOM_CSS_CLASSES,
    }

def get_quick_questions_by_category(category: str) -> List[Dict]:
    """Get quick questions for a specific category."""
    return QUICK_QUESTIONS_CONFIG.get(category, {}).get("questions", [])

def get_all_quick_questions() -> List[Dict]:
    """Get all quick questions from all categories."""
    all_questions = []
    for category_data in QUICK_QUESTIONS_CONFIG.values():
        all_questions.extend(category_data.get("questions", []))
    return all_questions

def update_config(section: str, key: str, value: Any) -> None:
    """
    Update a configuration value at runtime.

    Args:
        section: Configuration section (e.g., "chat", "features")
        key: Configuration key to update
        value: New value
    """
    config_map = {
        "chat": CHAT_CONFIG,
        "input_phase": INPUT_PHASE_CONFIG,
        "options": OPTIONS_CONFIG,
        "layout": LAYOUT_CONFIG,
        "animation": ANIMATION_CONFIG,
        "accessibility": ACCESSIBILITY_CONFIG,
        "features": FEATURE_FLAGS,
        "css_classes": CUSTOM_CSS_CLASSES,
    }

    if section in config_map:
        config_map[section][key] = value
    else:
        raise ValueError(f"Unknown configuration section: {section}")

# Validation functions
def validate_config() -> List[str]:
    """Validate configuration and return any errors."""
    errors = []

    # Validate depth range
    if OPTIONS_CONFIG["depth_range"][0] >= OPTIONS_CONFIG["depth_range"][1]:
        errors.append("Invalid depth range: minimum must be less than maximum")

    # Validate default depth
    min_depth, max_depth = OPTIONS_CONFIG["depth_range"]
    if not (min_depth <= OPTIONS_CONFIG["default_depth"] <= max_depth):
        errors.append(f"Default depth must be between {min_depth} and {max_depth}")

    # Validate default style
    if not set(OPTIONS_CONFIG["default_style"]).issubset(set(OPTIONS_CONFIG["available_styles"])):
        errors.append("Default style contains invalid options")

    return errors