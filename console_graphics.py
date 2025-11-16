ticks = "▁▂▃▄▅▆▇█"

def spark(values):
    mn, mx = min(values), max(values)
    scale = mx - mn if mx != mn else 1
    return "".join(ticks[int((v - mn) / scale * (len(ticks) - 1))] for v in values)