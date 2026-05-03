def score_stock(f):

    score = 0

    # ---------------------------
    # VALUE (drawdown)
    # ---------------------------
    if f["drawdown"] > 20:
        score += 35
    elif f["drawdown"] > 10:
        score += 25
    elif f["drawdown"] > 5:
        score += 15

    # ---------------------------
    # RECOVERY POTENTIAL
    # ---------------------------
    score += f["recovery"] * 0.5

    # ---------------------------
    # STABILITY
    # ---------------------------
    if f["volatility"] < 3:
        score += 15

    # ---------------------------
    # TREND QUALITY
    # ---------------------------
    if f["trend"] > 0:
        score += 15
    else:
        score -= 10

    return round(min(100, score), 2)
