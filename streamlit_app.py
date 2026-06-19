import streamlit as st

from src.classifier import classify_persona
from src.generator import generate_response
from src.rag_pipeline import LocalRAGPipeline
from src.escalator import should_escalate
from src.handoff import generate_handoff_summary


# Initialize RAG pipeline
rag = LocalRAGPipeline()

# Load documents and create chunks
rag.load_documents()
rag.chunk_documents()

# Store embeddings only once
if rag.collection.count() == 0:
    rag.ingest_chunks()


st.title("Persona-Adaptive Customer Support Agent")

query = st.text_input("Enter your issue")

if st.button("Submit"):

    # Persona detection
    persona_result = classify_persona(query)
    persona = persona_result["persona"]

    # Retrieve relevant chunks
    retrieved_chunks = rag.retrieve(query)

    # Escalation check
    escalate = should_escalate(
        query,
        retrieved_chunks
    )

    # Build context
    context = "\n\n".join(
        chunk["text"]
        for chunk in retrieved_chunks
    )

    # Generate response
    response = generate_response(
        query,
        persona,
        context
    )

    # Display results
    st.subheader("Detected Persona")
    st.write(persona)

    st.subheader("Escalation Status")
    st.write(escalate)

    st.subheader("Response")
    st.write(response)

    st.subheader("Retrieved Sources")

    if retrieved_chunks:
        for chunk in retrieved_chunks:
            st.write(chunk["source"])
    else:
        st.write("No documents retrieved.")

    # Human handoff summary
    if escalate:
        handoff_summary = generate_handoff_summary(
            persona,
            query,
            retrieved_chunks
        )

        st.subheader("Human Handoff Summary")
        st.json(handoff_summary)