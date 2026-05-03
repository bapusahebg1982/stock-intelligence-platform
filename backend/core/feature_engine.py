def compute_features(price, peak):

    if not peak or peak <= 0:
        return None

    drawdown = ((peak - price) / peak) * 100

    # realistic volatility proxy
    volatility = min(5, max(1, drawdown / 8))

    # momentum signal
    momentum = -1 if drawdown > 15 else 1

    return {
        "drawdown": round(drawdown, 2),
        "volatility": round(volatility, 2),
        "momentum": momentum
    }
