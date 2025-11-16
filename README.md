# 💬 VibeCheck, AI-Powered WhatsApp Chat Analyzer

## 📌 Overview
**VibeCheck** is a Python-based analytics engine that transforms exported WhatsApp chats into **relationship insights, emotional intelligence summaries, and vibe patterns**.

It combines classical statistics, sentiment analysis, and LLM-powered reasoning to generate **per-person**, **per-session**, and **entire conversation** reports revealing texting habits, emotions, and connection dynamics.

---

## 🚀 Features

### 🔹 User-Level Analytics
For each participant:
- 🕰️ Avg response time  
- 💬 Single vs double texting ratio  
- 🗣 Avg text volume  
- 🔢 Total messages sent  
- 😶 Dry text ratio  
- 🖼️ Media/sticker frequency  
- 🧭 Initiation rate  
- 🕛 Hour heatmap  

### 🔹 Session-Level Analytics
Each session (≥45 min silence = new session) includes:
- Session timing + duration  
- Messages & reply speeds per user  
- Message balance ratio  
- Double-text streak behavior  
- Sentiment breakdown (positive / neutral / negative)  
- Sentiment trend (rising / cooling / recovering / stable / falling)  
- Most positive & most negative messages  
- **LLM Emotional Interpretation:**
  - Topic  
  - Summary  
  - Tone  
  - Vibe tag  
  - Message intent  
  - Relationship signal  
  - Emotion keywords  
  - Advice  

### 🔹 Conversation Summary
- Longest streak of daily texting  
- Longest texting gap  
- Total number of sessions  
- Full comparison of both users  
- Overall vibe evolution across sessions  

---

## 🧠 How It Works

| Layer | Role |
|-------|------|
| Parser | Converts WhatsApp .txt export to structured messages |
| Metrics | Behavioral statistics (response time, dry %, double texts, etc.) |
| Sentiment Model | Multilingual transformer (`twitter-xlm-roberta-base-sentiment`) |
| NLP | Tone / trend / emotional spikes |
| LLM | High-level interpretation and advice |
| Report | Console + `.txt` export |

### Tech Stack
| Component | Tool |
|----------|-----|
| Language | Python |
| Transformer | Hugging Face (RoBERTa multilingual) |
| LLM API | OpenRouter (Llama-3.3-70B-Instruct) |
| Env Management | python-dotenv |

---

## 🔧 Installation

1. Install dependencies
```
pip install -r requirements.txt
```

2. Add API Key
Create `.env`:
```
OPENROUTER_API_KEY=your_openrouter_key
```

3. Add your .txt file within `./personal_dataset` folder 

4. Run program
```
python main.py
```

---

## ▶️ Example Output

```
📌 Conversation file: X.txt

👤 X REPORT
--------------
🕛 Avg response time: 78.50 min
💬 Single : Double texts = 66.3% : 33.7%
📏 Avg text volume: 23 character per message
☯️ Total text sent: 156 messages
💦 Dry text ratio: 24.2% dry texts
🖼️ Total Media+stickers sent: 24
🔥 Initiation rate: 38.9%
⌛Hour Heatmap: ▅▂▂▂▂▁▁▁▁▂▅▅▂▁▃▂▁▁▁▂▃▃▅█

👤 Y REPORT
--------------
🕛 Avg response time: 306.69 min
💬 Single : Double texts = 42.3% : 57.7%
📏 Avg text volume: 33 character per message
☯️ Total text sent: 234 messages
💦 Dry text ratio: 13.2% dry texts
🖼️ Total Media+stickers sent: 29
🔥 Initiation rate: 61.1%
⌛Hour Heatmap: ▄▃▂▃▃▁▁▁▁▄▃▄▁▃▃▂▁▁▁▄▃█▄▆

📊 Summary
--------------
➡️  Faster replier: X
➡️  More double-texts: Y
➡️  More character per message: Y
➡️  More texts sent: Y
➡️  More Media sent: Y
➡️  More Dry texts: X
➡️  Total Chat Sessions: 36
➡️  Total texts sent: 390
➡️  Min/Avg/Max Session Length: 1/8/49 messages
➡️  Longest texting streak: 5 days
➡️  Longest texting gap: 69 days
➡️  More Initiation Rate: Y

🎉 Per Session REPORT
--------------
SESSION 1 - 15/07/2025, 14:35 to 15/07/2025, 15:38
--------------
👤 X REPORT
--------------
🕛 Avg response time: 1.60 min
💬 Single : Double texts = 57.1% : 42.9%
📏 Avg text volume: 15 character per message
☯️ Total text sent: 31 messages
💦 Dry text ratio: 34.4% dry texts
🖼️ Total Media+stickers sent: 0
😍 [SENTIMENT] Overall Sentiment: neutral
😍 [SENTIMENT] Overall trend: recovering
😍 [SENTIMENT] higesht positive text: It looks so cool
😍 [SENTIMENT] higesht negative text: I'm bossy around everyone

👤 Y REPORT
--------------
🕛 Avg response time: 0.65 min
💬 Single : Double texts = 65.0% : 35.0%
📏 Avg text volume: 35 character per message
☯️ Total text sent: 34 messages
💦 Dry text ratio: 20.0% dry texts
🖼️ Total Media+stickers sent: 0
😍 [SENTIMENT] Overall Sentiment: neutral
😍 [SENTIMENT] Overall trend: rising
😍 [SENTIMENT] higesht positive text: Yayyy
😍 [SENTIMENT] higesht negative text: 1lakh snaps 😨

📊 Summary
--------------
➡️  Faster replier: Y
➡️  More double-texts: X
➡️  More character per message: Y
➡️  More texts sent: Y
➡️  More Media sent: Y
➡️  More Dry texts: X
➡️  Total texts sent: 65
➡️ [LLM] Topic: New phone and horoscope discussion
➡️ [LLM] Summary: X and Y discuss Y's new phone, X's horoscope, and their personalities. They also talk about their interests and share some laughs. The conversation is light-hearted and playful, with a touch of teasing. They bond over their shared experiences and interests.
➡️ [LLM] Tone: playful
➡️ [LLM] Vibe: fun
➡️ [LLM] Message Intent: bonding
➡️ [LLM] relationship signal: closeness
➡️ [LLM] emotion_keywords: excitement teasing laughter
➡️ [LLM] Advice: Continue to be genuine and playful in your interactions to strengthen your bond.
```

---

## 🛡 Disclaimer
This project is for **personal reflection and fun** only.  
Do **not** use for harassment, stalking, or unauthorized monitoring.

---

## 🧑‍💻 Author
**Krish Sharma**
🌐 https://krishsharma.in
