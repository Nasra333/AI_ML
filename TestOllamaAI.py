
import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from IPython.display import display, Markdown
import ollama

load_dotenv(override=True)
# Initialize Ollama client

api_base = "http://localhost:11434/api/chat"
api_version = "v1"
headers = {"Content-Type": "application/json"}
models = "llama3.2"

message = "Hello, Llama! What is the capital of Nigeria?"
print(message)

response = ollama.chat(model= models, messages=[{"role": "user", "content": message}])
print("\n" + response["message"]["content"])

message = "Hello, Llama! Describe the process of photosynthesis."
payload = {    "model": models,
    "messages": [{"role": "user", "content": message}],
    "stream": False}
response = requests.post(f"{api_base}", headers=headers, json=payload)
print(Markdown(response.json()["message"]["content"]).data)

