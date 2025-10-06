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
PORT=7860
GRADIO_SERVER_NAME=0.0.0.0
```

## Deployment to Railway

### Prerequisites
- A [Railway](https://railway.app/) account
- Your API keys for OpenAI, Anthropic, and Google AI

### Deployment Steps

1. **Connect Your Repository**
   - Go to [Railway](https://railway.app/)
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose this repository

2. **Configure Environment Variables**
   In Railway's project settings, add the following environment variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   GOOGLE_API_KEY=your_google_api_key
   PORT=7860
   GRADIO_SERVER_NAME=0.0.0.0
   ```

3. **Deploy**
   - Railway will automatically detect the `Procfile` and `railway.json`
   - The build process will install dependencies from `requirements.txt`
   - Your app will be deployed and accessible via the Railway-provided URL

4. **Access Your Application**
   - Once deployed, Railway will provide a public URL
   - Click on the URL to access your Gradio application

### Railway Configuration Files

This project includes:
- **`Procfile`**: Defines the command to start the application
- **`railway.json`**: Railway-specific configuration for build and deploy settings
- **`.env.example`**: Template for required environment variables

### Troubleshooting

- **Build Failures**: Check Railway logs for dependency issues
- **Runtime Errors**: Verify all environment variables are set correctly
- **API Errors**: Ensure your API keys are valid and have sufficient credits
