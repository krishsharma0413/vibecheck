from datetime import datetime
import re

msg_pattern = re.compile(r"^\d{2}/\d{2}/\d{4}, \d{2}:\d{2} - .*?:") # helps skip faltu lines
fmt = "%d/%m/%Y, %H:%M"

def response_time(texts, username):
    """
    texts: all texts from the whatsapp chat export
    username: username of the user we are trying to find the response time for
    """
    last_sender = ""
    total_delay = 0
    reply_count = 0
    last_sender = None
    last_time = None
        
    splitter = f" - {username}:"
    for x in texts:
        if not msg_pattern.match(x):
            continue
        try:
            timestamp = datetime.strptime(x[:17], fmt)
        except:
            # an error means some other kind of text
            continue
        if splitter in x:
            sender = "user"            
        else:
            sender = "other"
        
        if sender == "user" and last_sender == "other":
            total_delay += (timestamp - last_time).total_seconds()
            reply_count += 1
        
        last_sender = sender
        last_time = timestamp
    
    return total_delay / reply_count if reply_count > 0 else 0      

def single_double_text_rate(texts, username):
    user_turn = f" - {username}:"
    single = 0
    double = 0
    streak = 0
    last_sender = None

    for x in texts:
        sender = "user" if user_turn in x else "other"

        if sender == "user":
            streak += 1
        else:
            if streak == 1:
                single += 1
            elif streak > 1:
                double += 1
            streak = 0
        
        last_sender = sender

    if streak == 1:
        single += 1
    elif streak > 1:
        double += 1

    total = single + double
    return [single/total if total > 0 else 0, double/total if total > 0 else 0]


def avg_text_volumne(texts, username):
    """
    tells whats the average length of their text
    """
    splitter = f" - {username}:"
    text_count = 1
    size = 0
    for x in texts:
        if splitter in x:
            text_count += 1
            size += len(x.split(splitter)[1])
    
    return size/text_count

def total_texts_sent(texts, username):
    """
    raw number of how many text the user has sent
    """
    count = 0
    splitter = f" - {username}:"
    for x in texts:
        if splitter in x:
            count += 1
    return count

def dry_text_ratio(texts, username):
    """
    ratio of how much the user dry text compared to normal texts
    dry text is text with less than 10 characters
    """
    total_count = 1
    dry_texts = 0
    splitter = f" - {username}:"
    for x in texts:
        if splitter in x:
            total_count += 1
            if len(x.split(splitter)[1]) < 10:
                dry_texts += 1
    return dry_texts/total_count

def session_count(texts):
    """
    Amount of sessions that have occured between the users
    """
    count = 1
    last_time:datetime = None
    for x in texts:
        timestamp = datetime.strptime(x[:17], fmt)
        if last_time != None:
            if (timestamp - last_time).total_seconds() >= 2700:
                count += 1
        last_time = timestamp
    
    return count

def min_max_avg_session_length(texts):
    """
    session length is decided by the amt of messages in the 45min window before inactivity
    """
    sessions = []
    current_session_len = 0
    last_time = None

    for x in texts:
        try:
            timestamp = datetime.strptime(x[:16], fmt)
        except:
            continue

        if last_time is not None:
            gap = (timestamp - last_time).total_seconds()
            if gap >= 2700:  # 45 min gap → new session
                sessions.append(current_session_len)
                current_session_len = 0

        current_session_len += 1
        last_time = timestamp

    if current_session_len > 0:
        sessions.append(current_session_len)

    return min(sessions), max(sessions), sum(sessions)/len(sessions)

def total_media_count(texts, username):
    """
    total amount of media sent by the username. it includes media and stickers
    """
    count = 0
    splitter = f" - {username}:"
    for x in texts:
        if splitter in x and "<Media omitted>" in x:
            count += 1
    
    return count

def longest_day_streak(texts):
    """
    tells the longest streak of days the conversation happened
    """
    current_streak = 1
    last = None
    fmt = "%d/%m/%Y"
    max_streak = 0
    for x in texts:
        try:
            timestamp = datetime.strptime(x[:10], fmt)
        except:
            continue
        if last == None:
            last = timestamp
            continue
        
        if (timestamp - last).total_seconds() == 86400:
            current_streak += 1
        elif (timestamp - last).total_seconds() == 0:
            continue
        else:
            max_streak = max(max_streak, current_streak)
            current_streak = 1
        last = timestamp
    max_streak = max(max_streak, current_streak)
    return max_streak

def longest_day_gap(texts):
    """
    tells the longest gap of days between the conversation restarted again
    """
    last = None
    fmt = "%d/%m/%Y"
    max_gap = 0
    for x in texts:
        try:
            timestamp = datetime.strptime(x[:10], fmt)
        except:
            continue
        if last == None:
            last = timestamp
            continue
        
        if (timestamp - last).total_seconds() == 0:
            continue
        else:
            max_gap = max(max_gap, (timestamp - last).total_seconds())
        last = timestamp
    max_gap = max(max_gap, (timestamp - last).total_seconds())
    return max(int(max_gap/86400)-1, 0)


def initiation_rate(texts, username):
    """
    percentage of chats / sessions initiated by the username
    """
    fmt = "%d/%m/%Y, %H:%M"
    splitter = f" - {username}:"

    last_time = None
    sessions_started_by_user = 0
    total_sessions = 0
    expecting_starter = True

    for x in texts:
        timestamp = datetime.strptime(x[:17], fmt)

        if last_time is not None:
            if (timestamp - last_time).total_seconds() >= 2700:
                expecting_starter = True
                total_sessions += 1

        if expecting_starter:
            if splitter in x:
                sessions_started_by_user += 1
            expecting_starter = False

        last_time = timestamp

    total_sessions += 1

    return sessions_started_by_user / total_sessions


def user_hour_heatmap(texts, username):
    """
    For each hour of day (0-23), count how many DAYS the user was active.
    If user sends multiple messages in the same hour on the same day → count once.
    """
    hours = [0] * 24
    hours_taken = set()
    fmt = "%d/%m/%Y, %H:%M"
    day = None

    for x in texts:
        if f" - {username}:" not in x:
            continue

        timestamp = datetime.strptime(x[:17], fmt)

        if day is None or timestamp.date() != day.date():
            day = timestamp
            hours_taken = set()

        hour = timestamp.hour
        if hour not in hours_taken:
            hours[hour] += 1
            hours_taken.add(hour)

    return hours
