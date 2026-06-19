import chromadb
from google import genai

from src.config import GEMINI_API_KEY

from pathlib import Path

from langchain_text_splitters import RecursiveCharacterTextSplitter


class LocalRAGPipeline:
    def __init__(self):
        self.documents = []

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=400,
            chunk_overlap=40
        )

        self.chunks = []

        self.client = genai.Client(api_key=GEMINI_API_KEY)

        self.chroma_client = chromadb.PersistentClient(path="./chroma_db")

        self.collection = self.chroma_client.get_or_create_collection(
            name="support_kb"
        )


    def load_documents(self):
        data_folder = Path("data")

        for file in data_folder.glob("*.txt"):
            with open(file, "r", encoding="utf-8") as f:
                text = f.read()

                self.documents.append({
                    "source": file.name,
                    "content": text
                })

        return self.documents

    def chunk_documents(self):
        for doc in self.documents:
            split_chunks = self.text_splitter.split_text(doc["content"])

            for index, chunk in enumerate(split_chunks):
                self.chunks.append({
                    "text": chunk,
                    "source": doc["source"],
                    "chunk_index": index
                })

        return self.chunks

    def get_embedding(self, text):
        response = self.client.models.embed_content(
            model="gemini-embedding-001",
            contents=text
        )

        return response.embeddings[0].values  

    def ingest_chunks(self):
        for chunk in self.chunks:
            embedding = self.get_embedding(chunk["text"])

            chunk_id = (
                f"{chunk['source']}_{chunk['chunk_index']}"
            )

            self.collection.add(
                ids=[chunk_id],
                embeddings=[embedding],
                documents=[chunk["text"]],
                metadatas=[
                    {
                        "source": chunk["source"],
                        "chunk_index": chunk["chunk_index"]
                    }
                ]
            )    

    def retrieve(self, query, top_k=3):
        query_embedding = self.get_embedding(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )

        retrieved_chunks = []

        documents = results["documents"][0]
        metadatas = results["metadatas"][0]

        for doc, metadata in zip(documents, metadatas):
            retrieved_chunks.append({
                "text": doc,
                "source": metadata["source"]
            })

        return retrieved_chunks