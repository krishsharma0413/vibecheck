from dotenv import load_dotenv, dotenv_values
import requests
import json

load_dotenv(".env")
ENV = dotenv_values(".env")
OPENROUTER_API_KEY = ENV["OPENROUTER_API_KEY"]


def system_prompt(texts, past_topic, past_summary):
    system = f"""
You are a chat analyst. Analyze the following chat between two users and return only a Python-parsable dict (JSON-like) with no extra text.

CHAT HISTORY
------------
{texts}

PREVIOUS CHAT SESSION CONTEXT
-----------------------------
Previous chat between the user had following information.
TOPIC: {past_topic}
SUMMARY: {past_summary}

RETURN ONLY THIS STRUCTURE
--------------------------
{{
  "chat_topic": "<short topic, max 20 words>",
  "chat_summary": "<2-4 sentence summary of the conversation>",
  "tone": "<emotional tone e.g. warm, playful, dry, tense, awkward>",
  "vibe_tag": "<one-word vibe e.g. flirty, fun, serious, emotional, conflict, supportive> (not limited to these)",
  "message_intent": "<purpose of messages, e.g. planning, bonding, teasing, resolving issues> (not limited to these)",
  "relationship_signal": "<what the session indicates about closeness / distance>",
  "emotion_keywords": ["<keyword1>", "<keyword2>", "<keyword3>"],
  "advice": "<1 sentence behavioural suggestion related to chat>",
  "previous_session_relevance": bool<true or false>, // is this conversation relevant to the past chat session? 
}}

IMPORTANT:
- No commentary
- No markdown formatting
- Do not escape quotes
- Only return the dict, not prose
"""
    return system


def call_llm(texts, past_topic, past_summary):
    response = requests.post(
    url="https://openrouter.ai/api/v1/chat/completions",
    headers={
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "krishsharma.in",
        "X-Title": "Krish Sharma",
    },
    data=json.dumps({
        "model": "meta-llama/llama-3.3-70b-instruct:free",
        "messages": [
            {
            "role": "system",
            "content": system_prompt(texts, past_topic, past_summary)
            }
        ]
    })
    )
    
    print(response.json()["choices"][0]["message"]["content"])