from dotenv import load_dotenv, dotenv_values
import requests
import json

load_dotenv(".env")
ENV = dotenv_values(".env")
OPENROUTER_API_KEY = ENV["OPENROUTER_API_KEY"]


def llm_chat_history_formatter(texts, user1, user2):
    resp = ""
    splitter1 = f" - {user1}:"
    splitter2 = f" - {user2}:"
    for x in texts:
        if splitter1 in x:
            resp += "A: " + x.split(splitter1)[1]
        if splitter2 in x:
            resp += "B: " + x.split(splitter2)[1]
    return resp

def system_prompt(texts, past_topic, past_summary, user1, user2):
    system = f"""
You are a chat analyst. Analyze the following chat between two users and return only a Python-parsable dict (JSON-like) with no extra text.

USERS
-----
history has A & B for names, generate report according to the real names
A is {user1}
B is {user2}

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


def call_llm(texts, past_topic, past_summary, u1, u2):
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
            "content": system_prompt(texts, past_topic, past_summary, u1, u2)
            }
        ]
    })
    )
    
    try:
        content = response.json()["choices"][0]["message"]["content"].strip()
        content = content.replace("```json", "").replace("```", "")
        # print(response.json())
        return json.loads(content)
    except Exception as e:
        # print(e)
        return {}
    
# print(call_llm(llm_chat_history_formatter("", "none", "none"), "no pas convo", "no pas convo", "none", "none"))