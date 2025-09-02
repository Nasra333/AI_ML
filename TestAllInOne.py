
import os
import requests
from openai import OpenAI
from openai import OpenAIError
import anthropic as anthropicai
import google.generativeai as genai
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import List, Dict, Any
import gradio as gr
from datetime import datetime


load_dotenv(override=True)
# Initialize OpenAI client
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
anthropic = anthropicai.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))


system_pronpt = [{"role": "system", "content": "You are a comedian that tell jokes."}]
user_prompt = [{"role": "user", "content": "Tell me a joke about cats."}]

def callOpenAI(input: str):
    prompt = [
            {"role": "system", "content": "You are a comedian that tell jokes."},
            {"role": "user", "content": input}
        ]

    response = openai.chat.completions.create(model = "gpt-4o-mini", messages=prompt)
    return "\n" + response.choices[0].message.content

def streamOpenAI(system: str, question: str):
    prompt = [
            {"role": "system", "content": system if system is not None else "You are a comedian that tell jokes."},
            {"role": "user", "content": question}
        ]
    
    result: str = ""
    response = openai.chat.completions.create(
        model = "gpt-4o-mini", 
        messages=prompt
        , stream=True)
    for chunk in response:
        result += chunk.choices[0].delta.content or ""
        yield result

def callClaude():
    response = anthropic.messages.create(
        model="claude-opus-4-1-20250805",
        max_tokens=1024,
        temperature=0.7,
        system="You are a comedian that tell jokes.",
        messages=[
            {"role": "user", "content": "Tell me a joke about Racoons."}
        ]
    )
    print(response.content[0].text)

def streamClaude(system: str, message: str):
    response = anthropic.messages.stream(
        model="claude-opus-4-1-20250805",
        max_tokens=1024,
        temperature=0.7,
        system = system if system is not None else "You are a comedian that tell jokes.",
        messages = [
            {"role": "user", "content": message}
        ]
    )
    result: str = ""
    with response as stream:
        for chunk in stream.text_stream:
            result += chunk
            yield result

def callGemini():
    gemini = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction= system_pronpt[0]['content']
    )
    response = gemini.generate_content(contents="Tell me a joke about Racoons.")
    print(response.text)

#callGemini() 

gr.Interface(
    fn=streamClaude,
    inputs=[
        gr.Textbox(label="System", lines=2, placeholder="Enter your system prompt here..."),
        gr.Textbox(label="Question", lines=2, placeholder="Enter your prompt here...")
        ],
    outputs=[gr.Markdown(label="Response")],
    title="OpenAI GPT-4o-Mini",
    description="Call OpenAI's GPT-4o-Mini model to tell a joke about Racoons.",
    flagging_mode="manual"
).launch(share=True)