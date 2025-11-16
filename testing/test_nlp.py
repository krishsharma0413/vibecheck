from transformers import AutoModelForSequenceClassification, XLMRobertaTokenizer
import torch

model_path = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

tokenizer = XLMRobertaTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)

labels = ["negative", "neutral", "positive"]

def sentiment(text):
    encoded = tokenizer(text, return_tensors="pt", truncation=True)
    logits = model(**encoded).logits
    prob = torch.softmax(logits, dim=1)[0].tolist()
    return {"label": labels[prob.index(max(prob))], "scores": dict(zip(labels, prob))}

print(sentiment("love you bhai"))
