def score_stock(features):

    score = 0

    # value opportunity
    if features["drawdown"] > 30:
        score += 40
    elif features["drawdown"] > 15:
        score += 25

    # stability
    if features["volatility"] < 3:
        score += 25

    # momentum
    if features["momentum"] > 0:
        score += 20

    return min(score, 100)
