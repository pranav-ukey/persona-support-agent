from src.classifier import classify_persona
from src.generator import generate_response
from src.rag_pipeline import LocalRAGPipeline
from src.escalator import should_escalate
from src.handoff import generate_handoff_summary

# Initialize RAG pipeline
rag = LocalRAGPipeline()

# Load documents
rag.load_documents()

# Create chunks
rag.chunk_documents()

# User query
query = input("Enter query: ")

# Detect persona
persona_result = classify_persona(query)
persona = persona_result["persona"]

# Retrieve relevant chunks
retrieved_chunks = rag.retrieve(query)

# Escalation check
escalate = should_escalate(
    query,
    retrieved_chunks
)

# Build context for Gemini
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

# Output
print("\nPersona:")
print(persona)

print("\nEscalation Status:")
print(escalate)

print("\nResponse:")
print(response)

# Human handoff summary
if escalate:
    handoff_summary = generate_handoff_summary(
        persona,
        query,
        retrieved_chunks
    )

    print("\nHuman Handoff Summary:")
    print(handoff_summary)