import os
from whoami import name
from file_parser import text_file_parser, participants
from stats import response_time, single_double_text_rate, avg_text_volumne
from stats import total_texts_sent, dry_text_ratio, session_count, min_max_avg_session_length
from stats import total_media_count, longest_day_streak, longest_day_gap, initiation_rate
from stats import user_hour_heatmap
from console_graphics import spark

BASE_DIR = "./personal_dataset/"

for x in os.listdir(BASE_DIR):
    if x.endswith(".txt"):
        file_path = os.path.join(BASE_DIR, x)
        texts = text_file_parser(file_path)
        
        u1, u2 = participants(texts)

        rt1 = response_time(texts, u1)
        rt2 = response_time(texts, u2)

        s1, d1 = single_double_text_rate(texts, u1)
        s2, d2 = single_double_text_rate(texts, u2)
        
        v1 = avg_text_volumne(texts, u1)
        v2 = avg_text_volumne(texts, u2)
        
        t1 = total_texts_sent(texts, u1)
        t2 = total_texts_sent(texts, u2)
        
        dry1 = dry_text_ratio(texts, u1)
        dry2 = dry_text_ratio(texts, u2)
        
        min_session, max_session, avg_session = min_max_avg_session_length(texts)

        media1 = total_media_count(texts, u1)
        media2 = total_media_count(texts, u2)
        
        initiation_rate1 = initiation_rate(texts, u1)
        initiation_rate2 = initiation_rate(texts, u2)

        print(f"\n📌 Conversation file: {x}\n")

        print(f"👤 {u1} REPORT")
        print("--------------")
        print(f"⏱ Avg response time: {rt1/60:.2f} min")
        print(f"💬 Single : Double texts = {s1*100:.1f}% : {d1*100:.1f}%")
        print(f"📏 Avg text volume: {int(v1)} character per message")
        print(f"☯️ Total text sent: {t1} messages")
        print(f"💦 Dry text ratio: {dry1*100:.1f}% dry texts")
        print(f"🖼️ Total Media+stickers sent: {media1}")
        print(f"🔥 Initiation rate: {initiation_rate1*100:.1f}%")
        print(f"⌛Hour Heatmap: {spark(user_hour_heatmap(texts, u1))}")
        print()

        print(f"👤 {u2} REPORT")
        print("--------------")
        print(f"⏱ Avg response time: {rt2/60:.2f} min")
        print(f"💬 Single : Double texts = {s2*100:.1f}% : {d2*100:.1f}%")
        print(f"📏 Avg text volume: {int(v2)} character per message")
        print(f"☯️ Total text sent: {t2} messages")
        print(f"💦 Dry text ratio: {dry2*100:.1f}% dry texts")
        print(f"🖼️ Total Media+stickers sent: {media2}")
        print(f"🔥 Initiation rate: {initiation_rate2*100:.1f}%")
        print(f"⌛Hour Heatmap: {spark(user_hour_heatmap(texts, u2))}")
        print()

        faster = u1 if rt1 < rt2 else u2
        double_text_more = u1 if d1 > d2 else u2
        more_text_volume = u1 if v1 >= v2 else u2
        total_max = u1 if t1 > t2 else u2
        more_dry = u1 if dry1 > dry2 else u2
        more_media = u1 if media1 > media2 else u2
        more_initiation = u1 if initiation_rate1 > initiation_rate2 else u2

        print(f"📊 Summary")
        print("--------------")
        print(f"➡️  Faster replier: {faster}")
        print(f"➡️  More double-texts: {double_text_more}")
        print(f"➡️  More character per message: {more_text_volume}")
        print(f"➡️  More texts sent: {total_max}")
        print(f"➡️  More Media sent: {more_media}")
        print(f"➡️  More Dry texts: {more_dry}")
        print(f"➡️  Total Chat Sessions: {session_count(texts)}")
        print(f"➡️  Total texts sent: {t1+t2}")
        print(f"➡️  Min/Avg/Max Session Length: {min_session}/{int(avg_session)}/{max_session} messages")
        print(f"➡️  Longest texting streak: {longest_day_streak(texts)} days")
        print(f"➡️  Longest texting gap: {longest_day_gap(texts)} days")
        print(f"➡️  More Initiation Rate: {more_initiation}")
        print("\n--------------------------------------\n")
