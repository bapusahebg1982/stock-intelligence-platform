def compute_features(price, peak):

    if not peak or peak <= 0:
        return None

    drawdown = ((peak - price) / peak) * 100

    # better volatility scaling
    volatility = min(5, max(1, drawdown / 6))

    # recovery potential (bigger drop = more upside, but cap it)
    recovery = min(30, drawdown)

    # trend quality (penalize extreme drops)
    trend_score = 1 if drawdown < 25 else -1

    return {
        "drawdown": round(drawdown, 2),
        "volatility": round(volatility, 2),
        "recovery": round(recovery, 2),
        "trend": trend_score
    }
