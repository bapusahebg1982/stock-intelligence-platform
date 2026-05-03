def compute_features(price, peak):

    # ---------------------------
    # FIX 1: VALIDATE PEAK
    # ---------------------------
    if peak < price:
        peak = price * 1.2  # assume recent high above current

    # ---------------------------
    # DRAW DOWN (ALWAYS POSITIVE)
    # ---------------------------
    drawdown = ((peak - price) / peak) * 100

    # ---------------------------
    # VOLATILITY (SIMPLIFIED)
    # ---------------------------
    volatility = min(5, max(1, drawdown / 10))

    # ---------------------------
    # MOMENTUM (BASIC SIGNAL)
    # ---------------------------
    momentum = 1 if drawdown > 20 else -1

    return {
        "drawdown": round(drawdown, 2),
        "volatility": round(volatility, 2),
        "momentum": momentum
    }
