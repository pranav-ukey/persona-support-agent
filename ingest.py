from src.rag_pipeline import LocalRAGPipeline

rag = LocalRAGPipeline()

rag.load_documents()
rag.chunk_documents()
rag.ingest_chunks()

print("Knowledge base created successfully!")