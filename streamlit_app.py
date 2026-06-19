import streamlit as st

from src.classifier import classify_persona
from src.generator import generate_response
from src.rag_pipeline import LocalRAGPipeline
from src.escalator import should_escalate
from src.handoff import generate_handoff_summary


rag = LocalRAGPipeline()

rag.load_documents()
rag.chunk_documents()


st.title("Persona-Adaptive Customer Support Agent")

query = st.text_input("Enter your issue")

if st.button("Submit"):

    persona_result = classify_persona(query)

    persona = persona_result["persona"]

    retrieved_chunks = rag.retrieve(query)

    escalate = should_escalate(
        query,
        retrieved_chunks
    )

    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    response = generate_response(
        query,
        persona,
        context
    )

    st.subheader("Detected Persona")
    st.write(persona)

    st.subheader("Escalation Status")
    st.write(escalate)

    st.subheader("Response")
    st.write(response)

    st.subheader("Retrieved Sources")

    for chunk in retrieved_chunks:
        st.write(chunk["source"])

    if escalate:

        handoff_summary = generate_handoff_summary(
            persona,
            query,
            retrieved_chunks
        )

        st.subheader("Human Handoff Summary")

        st.json(handoff_summary)