def should_escalate(query, retrieved_chunks):
    sensitive_keywords = [
        "billing",
        "refund",
        "payment",
        "legal",
        "account deletion"
    ]

    query_lower = query.lower()

    for keyword in sensitive_keywords:
        if keyword in query_lower:
            return True

    if len(retrieved_chunks) == 0:
        return True

    return False