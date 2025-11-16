from transformers import AutoModelForSequenceClassification, XLMRobertaTokenizer
import torch

model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

tokenizer = XLMRobertaTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

labels = ['negative', 'neutral', 'positive']

def sentiment(text):
    encoded = tokenizer(text, return_tensors="pt", truncation=True)
    logits = model(**encoded).logits
    prob = torch.softmax(logits, dim=1)[0].tolist()
    return {"label": labels[prob.index(max(prob))], "scores": dict(zip(labels, prob))}


def texts_cleaner(texts):
    """
    texts has time that is not needed per session basis
    """
    return list(map(lambda x: x[20:], texts))

def user_session_sentiment(texts, username):
    texts = texts_cleaner(texts)
    user_prefix = f"{username}:"
    user_texts = [x.split(user_prefix, 1)[1].strip() for x in texts if x.startswith(user_prefix)]

    if len(user_texts) == 0:
        return "neutral", "stable", "", ""

    scores = [sentiment(x) for x in user_texts]

    pos_count = sum(1 for x in scores if x["label"] == "positive")
    neu_count = sum(1 for x in scores if x["label"] == "neutral")
    neg_count = sum(1 for x in scores if x["label"] == "negative")

    total = len(scores)
    distribution = [neg_count/total, neu_count/total, pos_count/total]
    

    overall = ["negative", "neutral", "positive"][distribution.index(max(distribution))]

    start = scores[0]["label"]
    end = scores[-1]["label"]
    trend = (
        "rising" if start in ["negative", "neutral"] and end == "positive" else
        "cooling" if start == "positive" and end in ["neutral", "negative"] else
        "falling" if start == "positive" and end == "negative" else
        "recovering" if start == "negative" and end == "neutral" else
        "stable"
    )

    highest_pos_msg = ""
    highest_neg_msg = ""
    max_pos = -1
    max_neg = -1
    for text, senti in zip(user_texts, scores):
        if senti["label"] == "positive" and senti["scores"]["positive"] > max_pos:
            max_pos = senti["scores"]["positive"]
            highest_pos_msg = text
        if senti["label"] == "negative" and senti["scores"]["negative"] > max_neg:
            max_neg = senti["scores"]["negative"]
            highest_neg_msg = text

    return overall, trend, highest_pos_msg, highest_neg_msg
