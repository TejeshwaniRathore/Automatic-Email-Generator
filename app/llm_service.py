# app/llm_service.py

import sys
import os
import json
from dotenv import load_dotenv
import requests

load_dotenv()

USE_OPENAI = os.getenv("OPENAI_API_KEY") is not None

if USE_OPENAI:
    try:
        from openai import OpenAI, RateLimitError
    except ImportError:
        print("OpenAI library not found. Please install with 'pip install openai'", file=sys.stderr)
        USE_OPENAI = False

# Groq fallback
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
USE_GROQ = GROQ_API_KEY is not None

if USE_GROQ:
    try:
        from groq import Groq
    except ImportError:
        print("Groq library not found. Please install with 'pip install groq'", file=sys.stderr)
        USE_GROQ = False
else:
    import requests


def generate_reply(conversation_history, sender, subject):
    prompt = f"""You are an AI assistant that generates email replies based on an entire email thread.

The full conversation history is provided below, with the newest email last.
Your task is to generate a reply to the LAST email in the thread, using the full conversation for context.

--- START OF EMAIL THREAD ---
{conversation_history}
--- END OF EMAIL THREAD ---

Based on the entire thread, create a JSON object for a reply to the last message. The JSON object must have two keys: "subject" and "body".
- The "subject" should be an appropriate reply subject line (e.g., "Re: {subject}").
- The "body" should be the email reply text, without any salutation or signature.

IMPORTANT: Respond with ONLY the JSON object, nothing else.

Example format:
{{
  "subject": "Re: Your Subject",
  "body": "This is the body of the email reply."
}}
"""

    llm_response_str = ""
    # 1. Try OpenAI
    if USE_OPENAI:
        client = OpenAI()
        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
            )
            llm_response_str = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"OpenAI error: {e}. Falling back to Groq.", file=sys.stderr)
    
    # 2. Try Groq if OpenAI failed or is not configured
    if not llm_response_str and USE_GROQ:
        print("Using Groq for reply generation.", file=sys.stderr)
        try:
            client = Groq(api_key=GROQ_API_KEY)
            response = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": "user", "content": prompt}],
            )
            llm_response_str = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Groq error: {e}. Falling back to Ollama.", file=sys.stderr)
    
    # 3. Fallback to Ollama if both OpenAI and Groq fail or aren't configured
    if not llm_response_str:
        print("Using Ollama for reply generation.", file=sys.stderr)
        model = os.getenv("OLLAMA_MODEL", "llama3")
        try:
            response = requests.post(
                "http://localhost:11434/api/generate",
                json={"model": model, "prompt": prompt, "stream": False},
            )
            llm_response_str = response.json().get("response", "").strip()
        except requests.ConnectionError as e:
            print(f"Failed to connect to Ollama: {e}", file=sys.stderr)

    # Parse the JSON response from the LLM
    try:
        # The LLM might wrap the JSON in markdown, so we clean it up.
        clean_json_str = llm_response_str.strip().removeprefix("```json").removesuffix("```")
        reply_json = json.loads(clean_json_str)
        if "subject" in reply_json and "body" in reply_json:
            return reply_json
    except (json.JSONDecodeError, AttributeError):
        print(f"Failed to parse JSON from LLM response: {llm_response_str}", file=sys.stderr)

    # Fallback in case of parsing failure
    return {"subject": f"Re: {subject}", "body": "Error: Could not generate a valid reply."}
