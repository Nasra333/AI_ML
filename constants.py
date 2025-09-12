
TAB_RECIPE = "TAB_RECIPE"
TAB_STUDY_NOTES = "TAB_STUDY_NOTES"
TAB_JOB_MATCH = "TAB_JOB_MATCH"
TAB_CODE_EXPLAINER = "TAB_CODE_EXPLAINER"
TAB_VIRTUAL_CASE_STUDY = "TAB_VIRTUAL_CASE_STUDY"

TAB_NAMES = {
    TAB_RECIPE: "Recipe Recommendation",
    TAB_STUDY_NOTES: "Study Notes Question And Answer",
    TAB_JOB_MATCH: "Basic Job Match Assistant",
    TAB_CODE_EXPLAINER: "Simple Code Explainer",
    TAB_VIRTUAL_CASE_STUDY: "Virtual Case Study Creator"
}

# Create a mapping for nicer default system prompts per tab (can be customized later)
default_system_prompts = {
    TAB_RECIPE: "You are a helpful chef assistant. Ask clarifying questions and suggest recipes.",
    TAB_STUDY_NOTES: "You help students with Q&A based on study notes. Keep answers concise and structured.",
    TAB_JOB_MATCH: "You assist with matching candidate skills to job descriptions and suggest improvements.",
    TAB_CODE_EXPLAINER: "You explain code in simple terms with step-by-step reasoning and examples.",
    TAB_VIRTUAL_CASE_STUDY: "You create realistic case studies with constraints and questions for analysis."
}


MODEL_OPEN_AI = "Open AI"
MODEL_CLAUD = "Claude AI"
MODEL_GEMINI = "Gemini AI"

modelChoices = [MODEL_OPEN_AI, MODEL_CLAUD, MODEL_GEMINI]
