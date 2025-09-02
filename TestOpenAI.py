import os
import requests
from openai import OpenAI
from openai import OpenAIError
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from typing import List, Dict, Any
from datetime import datetime
from IPython.display import display, Markdown


load_dotenv(override=True)
# Initialize OpenAI client
openai = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

message = "Hello, chatgpt!? who is Ikram Opeoluwa Samaad?"
print(message)

openai.api_base = "https://api.openai.com/v1"
openai.api_version = "2023-10-01"
openai.api_type = "openai"
openai.api_key = os.getenv("OPENAI_API_KEY")
response = openai.chat.completions.create(model = "gpt-4o-mini", messages=[{"role": "user", "content": message}])
print("\n" + response.choices[0].message.content)

x: int = 5
print(x)