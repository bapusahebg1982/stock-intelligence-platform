def search(q: str):

    q_norm = q.lower().strip()

    best_match = None
    best_score = 0

    for stock in STOCK_DB:

        name = stock["name"].lower()
        ticker = stock["ticker"].lower()

        # 🔥 EXACT TICKER MATCH = HIGHEST PRIORITY
        if q_norm.upper() == stock["ticker"].upper():
            return {"results": [stock]}

        score = 0

        if q_norm == name:
            score = 100
        elif q_norm in name:
            score = 80
        elif any(word in name for word in q_norm.split()):
            score = 50

        # 🔴 CRITICAL: penalize unrelated banks mixup
        if "bank" in q_norm and "bank" in name:
            score += 10

        if score > best_score:
            best_score = score
            best_match = stock

    # only return if confident
    if best_score >= 70:
        return {"results": [best_match]}

    return {"results": []}
