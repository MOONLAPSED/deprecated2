#! /app/app.py
import os
import requests, openai, os
from dotenv import load_dotenv
import os
import sys
import json
import requests
import openai


os.cmd = "pip install -U -r requirements.txt 2>&1 | tee error_log.txt"

# export OPENAI_API_BASE=http://localhost:8080
# export OPENAI_API_KEY=sk-420-69-1234
load_dotenv()
openai.api_base = "http://localhost:8080/v1"

def thing():
    prompt = ["Write a python program which provides the dot product of its arguments using only os and sys no imports"]
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "model": "orca-mini-7b.ggmlv3.q4_0.bin",
        "prompt": prompt,
        "temperature": 0.2
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.text)

def get_response(query):
  url = "http://localhost:8080/engine/text/generate"
  headers = {"Authorization": "Bearer sk-XXXXXXXXXXXXXXXXXXXX"}
  data = {"prompt": query}

  response = requests.post(url, headers=headers, data=data)

  return response.json()["choices"][0]["text"]

def main():
  query = input("Enter your query: ")
  response = get_response(query)

  print(response)

if __name__ == "__main__":
  main()

def run_api_request():
    url = "http://localhost:8080/v1/completions"
    prompt = ["Write a python program which provides the dot product of its arguments using only os and sys no imports"]
    headers = {
        "Content-Type": "application/json",
        # "Authorization": "Bearer " + rapidapi,
        # "My-Test-Header": "Testing!",
    }
    data = {
        "model": "orca-mini-7b.ggmlv3.q4_0.bin",
        "prompt": prompt,
        "temperature": 0.2
    }
    response = requests.post(url, headers=headers, json=data)
    print(response.text)
    print(response.json())
    print(response.encoding)
    print(response.content)

# run_chat_completion()
run_api_request()


# create a chat completion
def local_chat_completion(model, messages):
    # Replace with local API call
    return openai.ChatCompletion.create(model=model, messages=messages)

chat_completion = local_chat_completion(model="orca-mini-7b.ggmlv3.q4_0.bin", messages=[{"role": "user", "content": "Hello world"}])

