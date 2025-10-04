# AI_ML

A multi-tab AI application supporting various AI models (OpenAI, Anthropic, Google Generative AI, Ollama) with specialized interfaces for study notes Q&A and job matching.

## Project Setup

### Prerequisites
- Python 3.11 or higher
- pip (Python package installer)

### Installation

1. **Create a virtual environment (recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Running the Application

### Development Mode (with auto-reload)
For development with automatic file watching and hot-reload:
```bash
gradio app.py
```

### Production Mode
For standard execution:
```bash
python app.py
```

## Features

- **Multi-Model Support**: Switch between different AI providers (OpenAI, Anthropic, Google Generative AI, Ollama)
- **Hot Reload**: Instant updates during development
- **Tabbed Interface**: Specialized UI for different use cases

## Tabs Overview

### Study Notes Tab
Interactive Q&A system for study materials with document upload support.

**Features:**
- Upload documents or paste text
- Ask questions about your study notes
- Customizable answer styles (bullet points, numbered, flashcards)
- Adjustable detail levels

**Supported File Types:**
- Plain text (`.txt`)
- Markdown (`.md`)
- PDF documents (`.pdf`)
- Microsoft Word (`.docx`)

### Job Match Tab
Analyze compatibility between job descriptions and candidate profiles.

**Features:**
- Input job descriptions and candidate resumes
- Get match scores and analysis
- Identify skill gaps and suggestions
- [More features to be documented]

### Generic Tabs
General-purpose chat interfaces for various AI interactions.

**Features:**
- Basic chat functionality
- Model-specific system prompts
- [Additional features to be documented]

## Environment Variables

Create a `.env` file with your API keys:
```
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
GOOGLE_API_KEY=your_google_key
```
