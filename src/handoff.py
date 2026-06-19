def generate_handoff_summary(
    persona,
    query,
    retrieved_chunks
):
    return {
        "persona": persona,
        "issue": query,
        "documents_used": [
            chunk["source"]
            for chunk in retrieved_chunks
        ],
        "attempted_steps": [],
        "recommendation":
        "Investigate the issue manually."
    }