import os

import anthropic as anthropicai
import google.generativeai as genai
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(override=True)

# Initialize OpenAI client
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic = anthropicai.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

selectedModel: str = None
systemMessage: str = None

contextModelchanged: bool = False


def streamOpenAI(history: list):
    result: str = ""
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        stream=True)
    history.append({"role": "assistant", "content": ""})
    for chunk in response:
        result += chunk.choices[0].delta.content or ""
    for character in result:
        history[-1]['content'] += character
        yield history


def streamClaude(history: list):
    response = anthropic.messages.stream(
        model="claude-opus-4-1-20250805",
        max_tokens=1024,
        temperature=0.7,
        messages=history
    )
    result: str = ""
    with response as stream:
        for chunk in stream.text_stream:
            result += chunk
            yield result


def streamGemma(history: list):
    response = genai.chat.completions.create(
        model="gemini-1.5-pro",
        messages=history,
        temperature=0.7,
        max_output_tokens=1024,
        top_p=0.95,
        stream=True
    )
    result: str = ""
    history.append({"role": "assistant", "content": ""})
    for chunk in response:
        result += chunk.text or ""
        history[-1]['content'] += result
        yield history


def onModelChange(model: str):
    global selectedModel
    selectedModel = model
    global contextModelchanged
    contextModelchanged = True


def onSystemPromptChanged(prompt: str):
    global systemMessage
    systemMessage = prompt
    global contextModelchanged
    contextModelchanged = True


def userMessage(message: str, history: list):
    messages = []
    global contextModelchanged
    global systemMessage

    if contextModelchanged:
        history.clear()
        system_prompt = [{"role": "system",
                          "content": systemMessage if systemMessage is not None else "You are a comedian that tell jokes."}]
        messages = system_prompt
        contextModelchanged = False

    user_prompt = [{"role": "user", "content": message}]
    messages = history + user_prompt
    return "", messages


def responseStream(history: list):
    result: str = ""
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=history,
        stream=True)
    history.append({"role": "assistant", "content": ""})
    for chunk in response:
        result += chunk.choices[0].delta.content or ""
    for character in result:
        history[-1]['content'] += character
        yield history

