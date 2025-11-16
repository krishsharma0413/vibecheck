from stats import response_time, single_double_text_rate, avg_text_volumne
from stats import total_texts_sent, dry_text_ratio, session_count, min_max_avg_session_length
from stats import total_media_count, longest_day_streak, longest_day_gap, initiation_rate
from file_parser import participants
from session_nlp import user_session_sentiment
from api import call_llm, llm_chat_history_formatter

ticks = "▁▂▃▄▅▆▇█"

def spark(values):
    mn, mx = min(values), max(values)
    scale = mx - mn if mx != mn else 1
    return "".join(ticks[int((v - mn) / scale * (len(ticks) - 1))] for v in values)

def session_report(session_texts):
    past_topic = "No session exists previously"
    past_summary = "No session exists previously"
    for i, texts in enumerate(session_texts, start=1):
        
        
        print(f"SESSION {i} - {texts[0][:17]} to {texts[-1][:17]}")
        print("--------------")
        u1, u2 = participants(texts)
        u2_present = True
        if u2 == "":
            u2_present = False
        rt1 = response_time(texts, u1)
        if u2_present:
            rt2 = response_time(texts, u2)

        s1, d1 = single_double_text_rate(texts, u1)
        if u2_present:
            s2, d2 = single_double_text_rate(texts, u2)
        
        v1 = avg_text_volumne(texts, u1)
        if u2_present:
            v2 = avg_text_volumne(texts, u2)
        
        t1 = total_texts_sent(texts, u1)
        if u2_present:
            t2 = total_texts_sent(texts, u2)
        
        dry1 = dry_text_ratio(texts, u1)
        if u2_present:
            dry2 = dry_text_ratio(texts, u2)
        
        media1 = total_media_count(texts, u1)
        if u2_present:
            media2 = total_media_count(texts, u2)
            
        overall1, trend1, highest_pos_msg1, highest_neg_msg1 = user_session_sentiment(texts, u1)
        if u2_present:
            overall2, trend2, highest_pos_msg2, highest_neg_msg2 = user_session_sentiment(texts, u2)
        
                
        print(f"👤 {u1} REPORT")
        print("--------------")
        print(f"🕛 Avg response time: {rt1/60:.2f} min")
        print(f"💬 Single : Double texts = {s1*100:.1f}% : {d1*100:.1f}%")
        print(f"📏 Avg text volume: {int(v1)} character per message")
        print(f"☯️ Total text sent: {t1} messages")
        print(f"💦 Dry text ratio: {dry1*100:.1f}% dry texts")
        print(f"🖼️ Total Media+stickers sent: {media1}")
        print(f"😍 [SENTIMENT] Overall Sentiment: {overall1}")
        print(f"😍 [SENTIMENT] Overall trend: {trend1}")
        if highest_pos_msg1 != "":
            print(f"😍 [SENTIMENT] higesht positive text: {highest_pos_msg1}")
        if highest_neg_msg1 != "":
            print(f"😍 [SENTIMENT] higesht negative text: {highest_neg_msg1}")
        print()

        if u2_present:
            print(f"👤 {u2} REPORT")
            print("--------------")
            print(f"🕛 Avg response time: {rt2/60:.2f} min")
            print(f"💬 Single : Double texts = {s2*100:.1f}% : {d2*100:.1f}%")
            print(f"📏 Avg text volume: {int(v2)} character per message")
            print(f"☯️ Total text sent: {t2} messages")
            print(f"💦 Dry text ratio: {dry2*100:.1f}% dry texts")
            print(f"🖼️ Total Media+stickers sent: {media2}")
            print(f"😍 [SENTIMENT] Overall Sentiment: {overall2}")
            print(f"😍 [SENTIMENT] Overall trend: {trend2}")
            if highest_pos_msg2 != "":
                print(f"😍 [SENTIMENT] higesht positive text: {highest_pos_msg2}")
                
            if highest_neg_msg2 != "":
                print(f"😍 [SENTIMENT] higesht negative text: {highest_neg_msg2}")

            print()

            faster = u1 if rt1 < rt2 else u2
            double_text_more = u1 if d1 > d2 else u2
            more_text_volume = u1 if v1 >= v2 else u2
            total_max = u1 if t1 > t2 else u2
            more_dry = u1 if dry1 > dry2 else u2
            more_media = u1 if media1 > media2 else u2

            print(f"📊 Summary")
            print("--------------")
            print(f"➡️  Faster replier: {faster}")
            print(f"➡️  More double-texts: {double_text_more}")
            print(f"➡️  More character per message: {more_text_volume}")
            print(f"➡️  More texts sent: {total_max}")
            print(f"➡️  More Media sent: {more_media}")
            print(f"➡️  More Dry texts: {more_dry}")
            print(f"➡️  Total texts sent: {t1+t2}")
            

            # average llm enjoyer code
            chat_history = llm_chat_history_formatter(texts, u1, u2)
            llm_respose = call_llm(chat_history, past_topic, past_summary, u1, u2)
            
            if llm_respose.get("chat_topic", None):
                past_topic = llm_respose.get("chat_topic", "")
            
            if llm_respose.get("chat_summary", None):
                past_summary = llm_respose.get("chat_summary", "")

            if llm_respose.get("chat_topic", None):
                print(f'➡️ [LLM] Topic: {llm_respose.get("chat_topic", "")}')
            if llm_respose.get("chat_summary", None):
                print(f'➡️ [LLM] Summary: {llm_respose.get("chat_summary", "")}')
            if llm_respose.get("tone", None):
                print(f'➡️ [LLM] Tone: {llm_respose.get("tone", "")}')
            if llm_respose.get("vibe_tag", None):
                print(f'➡️ [LLM] Vibe: {llm_respose.get("vibe_tag", "")}')
            
            if llm_respose.get("message_intent", None):
                print(f'➡️ [LLM] Message Intent: {llm_respose.get("message_intent", "")}')
            if llm_respose.get("relationship_signal", None):
                print(f'➡️ [LLM] relationship signal: {llm_respose.get("relationship_signal", "")}')
            if llm_respose.get("emotion_keywords", None):
                print(f'➡️ [LLM] emotion_keywords: {" ".join(llm_respose.get("emotion_keywords", []))}')
            if llm_respose.get("advice", None):
                print(f'➡️ [LLM] Advice: {llm_respose.get("advice", "")}')
                
            if llm_respose.get("previous_session_relevance", None):
                print(f'➡️ [LLM] previous session relevance: {llm_respose.get("previous_session_relevance", "")}')

            print()

            