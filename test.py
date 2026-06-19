from src.classifier import classify_persona
from src.generator import generate_response
from src.rag_pipeline import LocalRAGPipeline

rag = LocalRAGPipeline()

rag.load_documents()
rag.chunk_documents()

query = input("Enter query: ")

persona_result = classify_persona(query)

persona = persona_result["persona"]

retrieved_chunks = rag.retrieve(query)

context = "\n\n".join(
    chunk["text"]
    for chunk in retrieved_chunks
)

response = generate_response(
    query,
    persona,
    context
)

print("\nPersona:")
print(persona)

print("\nResponse:")
print(response)