# Persona-Adaptive Customer Support Agent

## Project Overview

This project implements an AI-powered customer support agent that adapts its responses based on the user's persona. It uses Retrieval-Augmented Generation (RAG) to retrieve relevant information from a knowledge base and generate grounded responses. The system can also escalate unresolved issues to a human support agent and generate a structured handoff summary.

### Supported Personas

* Technical Expert
* Frustrated User
* Business Executive

### Features

* Persona detection
* Knowledge base retrieval using RAG
* Adaptive response generation
* ChromaDB vector database
* Gemini embeddings
* Human escalation logic
* Human handoff summary
* Interactive command-line chatbot
* Streamlit web interface
* TXT and PDF document support

## Tech Stack

### Language

* Python 3.11

### LLM

* Google Gemini 2.5 Flash Lite

### Embedding Model

* Gemini Embedding 001

### Vector Database

* ChromaDB

### Libraries

* google-genai
* chromadb
* langchain-text-splitters
* pypdf
* python-dotenv
* streamlit

## Project Structure

```text
persona-support-agent
│
├── data
├── src
├── chroma_db
├── app.py
├── ingest.py
├── streamlit_app.py
├── test.py
├── requirements.txt
├── README.md
```

## Architecture Diagram

```text
User Query
      ↓
Persona Detection
      ↓
Knowledge Retrieval (RAG)
      ↓
Response Generation
      ↓
Escalation Check
      ↓
Human Handoff Summary
```

## Persona Detection Strategy

The system classifies users into three personas:

### Technical Expert

Characteristics:

* Technical terminology
* Requests logs and API details
* Wants detailed explanations

Response style:

* Root cause analysis
* Technical terminology
* Step-by-step troubleshooting

### Frustrated User

Characteristics:

* Emotional language
* Repeated complaints
* Urgent requests

Response style:

* Empathetic
* Simple language
* Action-oriented

### Business Executive

Characteristics:

* Outcome-focused
* Minimal technical jargon
* Interested in business impact

Response style:

* Concise
* Impact-focused
* Estimated resolution guidance

## RAG Pipeline Design

### Document Loading

The system loads support documents from the `data` directory.

Supported formats:

* TXT
* PDF

### Chunking Strategy

Chunk Size:

* 400 characters

Chunk Overlap:

* 40 characters

### Embedding Model

* Gemini Embedding 001

### Vector Database

* ChromaDB

### Retrieval Strategy

* Semantic similarity search
* Top 3 relevant chunks are retrieved

## Escalation Logic

Conversations are escalated when:

* Billing issues are detected
* Refund requests are detected
* Legal issues are detected
* Account deletion requests are detected
* No suitable information is available

## Human Handoff Summary

The handoff summary contains:

* Detected persona
* User issue
* Retrieved documents used
* Attempted steps
* Recommendation for support engineers


## Setup Instructions

### Clone Repository

```bash
git clone <repository-url>
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```text
GEMINI_API_KEY=your_api_key
```

### Build Knowledge Base

```bash
python ingest.py
```

### Run CLI Application

```bash
python test.py
```

### Run Streamlit UI

```bash
python -m streamlit run streamlit_app.py
```

## Environment Variables

Required:

```text
GEMINI_API_KEY
```

## Example Queries

### Technical Expert

```text
My API key is giving a 401 Unauthorized error.
```

Expected Persona:

```text
Technical Expert
```

---

### Frustrated User

```text
I've tried everything and nothing works!
```

Expected Persona:

```text
Frustrated User
```

---

### Business Executive

```text
How will this issue impact operations and when will it be resolved?
```

Expected Persona:

```text
Business Executive
```

---

### Password Reset

```text
How do I reset my password?
```

---

### Refund Request

```text
I want a refund.
```

## Known Limitations

* Retrieval currently returns the top 3 chunks without confidence scoring.
* Persona detection may misclassify ambiguous queries.
* Multi-turn memory is not implemented.
* Human approval workflow is not implemented.
* Analytics dashboard is not implemented.

## Future Improvements

* Confidence scoring
* Multi-turn conversation memory
* LangGraph workflow
* Feedback collection system
* Human approval workflow
* Analytics dashboard
