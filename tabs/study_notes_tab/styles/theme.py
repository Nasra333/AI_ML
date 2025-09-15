"""
Design system and theme configuration for Study Notes Tab.
Provides consistent colors, spacing, typography, and design tokens.
"""

# Color Palette
COLORS = {
    # Primary Colors
    "primary": "#FF6B35",  # Orange (matches current Ask button)
    "primary_light": "#FF8A5A",
    "primary_dark": "#E55A2F",

    # Secondary Colors
    "secondary": "#4A90E2",
    "secondary_light": "#6BA3E7",
    "secondary_dark": "#3A7BC8",

    # Neutral Colors
    "gray_50": "#F9FAFB",
    "gray_100": "#F3F4F6",
    "gray_200": "#E5E7EB",
    "gray_300": "#D1D5DB",
    "gray_400": "#9CA3AF",
    "gray_500": "#6B7280",
    "gray_600": "#4B5563",
    "gray_700": "#374151",
    "gray_800": "#1F2937",
    "gray_900": "#111827",

    # Semantic Colors
    "success": "#10B981",
    "warning": "#F59E0B",
    "error": "#EF4444",
    "info": "#3B82F6",

    # Chat Colors
    "user_bg": "#EBF8FF",
    "assistant_bg": "#F7FAFC",
    "chat_border": "#E2E8F0",
}

# Spacing System (4px grid)
SPACING = {
    "xs": "0.25rem",    # 4px
    "sm": "0.5rem",     # 8px
    "md": "0.75rem",    # 12px
    "lg": "1rem",       # 16px
    "xl": "1.5rem",     # 24px
    "2xl": "2rem",      # 32px
    "3xl": "3rem",      # 48px
}

# Typography
TYPOGRAPHY = {
    "font_family": "system-ui, -apple-system, sans-serif",
    "font_sizes": {
        "xs": "0.75rem",    # 12px
        "sm": "0.875rem",   # 14px
        "base": "1rem",     # 16px
        "lg": "1.125rem",   # 18px
        "xl": "1.25rem",    # 20px
        "2xl": "1.5rem",    # 24px
    },
    "font_weights": {
        "normal": "400",
        "medium": "500",
        "semibold": "600",
        "bold": "700",
    },
    "line_heights": {
        "tight": "1.25",
        "normal": "1.5",
        "relaxed": "1.75",
    }
}

# Border Radius
RADIUS = {
    "none": "0",
    "sm": "0.125rem",   # 2px
    "md": "0.375rem",   # 6px
    "lg": "0.5rem",     # 8px
    "xl": "0.75rem",    # 12px
    "full": "9999px",
}

# Shadows
SHADOWS = {
    "sm": "0 1px 2px 0 rgb(0 0 0 / 0.05)",
    "md": "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
    "lg": "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
    "inner": "inset 0 2px 4px 0 rgb(0 0 0 / 0.05)",
}

# Component-specific styles
QUICK_BUTTON_STYLE = f"""
    background: {COLORS['gray_50']} !important;
    border: 1px solid {COLORS['gray_200']} !important;
    border-radius: {RADIUS['md']} !important;
    color: {COLORS['gray_700']} !important;
    font-weight: {TYPOGRAPHY['font_weights']['medium']} !important;
    padding: {SPACING['sm']} {SPACING['md']} !important;
    transition: all 0.2s ease !important;
    box-shadow: {SHADOWS['sm']} !important;
"""

QUICK_BUTTON_HOVER = f"""
    background: {COLORS['gray_100']} !important;
    border-color: {COLORS['gray_300']} !important;
    transform: translateY(-1px) !important;
    box-shadow: {SHADOWS['md']} !important;
"""

PRIMARY_BUTTON_STYLE = f"""
    background: {COLORS['primary']} !important;
    border: none !important;
    border-radius: {RADIUS['md']} !important;
    color: white !important;
    font-weight: {TYPOGRAPHY['font_weights']['semibold']} !important;
    padding: {SPACING['md']} {SPACING['xl']} !important;
    transition: all 0.2s ease !important;
    box-shadow: {SHADOWS['sm']} !important;
"""

SECONDARY_BUTTON_STYLE = f"""
    background: {COLORS['gray_100']} !important;
    border: 1px solid {COLORS['gray_300']} !important;
    border-radius: {RADIUS['md']} !important;
    color: {COLORS['gray_700']} !important;
    font-weight: {TYPOGRAPHY['font_weights']['medium']} !important;
    padding: {SPACING['sm']} {SPACING['lg']} !important;
    transition: all 0.2s ease !important;
"""

CHAT_CONTAINER_STYLE = f"""
    background: white !important;
    border: 1px solid {COLORS['gray_200']} !important;
    border-radius: {RADIUS['lg']} !important;
    box-shadow: {SHADOWS['sm']} !important;
    padding: {SPACING['lg']} !important;
    margin-bottom: {SPACING['lg']} !important;
"""

INPUT_CONTAINER_STYLE = f"""
    background: {COLORS['gray_50']} !important;
    border: 1px solid {COLORS['gray_200']} !important;
    border-radius: {RADIUS['lg']} !important;
    padding: {SPACING['lg']} !important;
    margin: {SPACING['md']} 0 !important;
"""

SECTION_HEADER_STYLE = f"""
    color: {COLORS['gray_800']} !important;
    font-size: {TYPOGRAPHY['font_sizes']['lg']} !important;
    font-weight: {TYPOGRAPHY['font_weights']['semibold']} !important;
    margin-bottom: {SPACING['md']} !important;
    line-height: {TYPOGRAPHY['line_heights']['tight']} !important;
"""

# Quick Questions Categories
QUICK_QUESTIONS_CONFIG = {
    "summary": {
        "title": "📋 Summary & Overview",
        "color": COLORS["info"],
        "questions": [
            {"icon": "📝", "text": "Summarize main points", "prompt": "Summarize the main points from my study notes."},
            {"icon": "🎯", "text": "Key takeaways", "prompt": "What are the most important takeaways from my study notes?"},
            {"icon": "🔍", "text": "Overview", "prompt": "Give me a comprehensive overview of my study notes."},
        ]
    },
    "study_tools": {
        "title": "🎓 Study Tools",
        "color": COLORS["success"],
        "questions": [
            {"icon": "🃏", "text": "Create flashcards", "prompt": "Create flashcards from the key concepts in my notes."},
            {"icon": "❓", "text": "Practice questions", "prompt": "Generate practice questions based on my study notes."},
            {"icon": "📊", "text": "Quiz me", "prompt": "Create a quiz to test my understanding of these notes."},
        ]
    },
    "analysis": {
        "title": "💡 Analysis & Understanding",
        "color": COLORS["secondary"],
        "questions": [
            {"icon": "💡", "text": "Explain concepts", "prompt": "Explain the key concepts from my study notes in simple terms."},
            {"icon": "🔗", "text": "Connections", "prompt": "What are the connections between different concepts in my notes?"},
            {"icon": "🤔", "text": "Clarify topics", "prompt": "Help me clarify any confusing topics from my notes."},
        ]
    }
}

def get_css_variables():
    """Generate CSS custom properties for the theme."""
    css_vars = []

    # Colors
    for name, value in COLORS.items():
        css_vars.append(f"--color-{name.replace('_', '-')}: {value};")

    # Spacing
    for name, value in SPACING.items():
        css_vars.append(f"--spacing-{name}: {value};")

    # Typography
    for category, values in TYPOGRAPHY.items():
        if isinstance(values, dict):
            for name, value in values.items():
                css_vars.append(f"--{category.replace('_', '-')}-{name.replace('_', '-')}: {value};")
        else:
            css_vars.append(f"--{category.replace('_', '-')}: {values};")

    # Radius
    for name, value in RADIUS.items():
        css_vars.append(f"--radius-{name}: {value};")

    return ":root { " + " ".join(css_vars) + " }"