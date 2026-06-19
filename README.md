# 🚀 Multi-Source AI Chatbot

An intelligent Retrieval-Augmented Generation (RAG) based chatbot that enables users to interact with information from multiple sources including **YouTube videos** and **PDF documents** using natural language queries.

The system extracts knowledge from uploaded documents or video transcripts, stores it in a vector database, retrieves the most relevant information, and generates context-aware responses using the **Llama 3.3 70B model powered by Groq**.

---

## 🌟 Project Highlights

* 📺 Chat with YouTube videos using transcript-based retrieval
* 📄 Chat with PDF documents and extract information instantly
* 🧠 Retrieval-Augmented Generation (RAG) architecture
* ⚡ Fast semantic search using FAISS Vector Database
* 🤖 Groq Llama 3.3 70B for response generation
* 🔍 Context-aware question answering
* 💬 Multi-turn conversation support
* 🚀 Optimized using model and vector database caching

---

# 📖 Problem Statement

Large documents and long video content often contain valuable information, but manually searching through them is time-consuming.

This project solves the problem by allowing users to ask questions directly in natural language. The chatbot automatically retrieves the most relevant information from PDFs or YouTube transcripts and generates accurate responses grounded in the source content.

---

# 🎯 Objectives

* Build a chatbot capable of understanding multiple knowledge sources.
* Implement a Retrieval-Augmented Generation (RAG) pipeline.
* Enable semantic search over unstructured text.
* Reduce hallucinations by grounding responses in retrieved context.
* Provide a simple and interactive user interface for querying documents and videos.

---

# 🏗️ System Architecture

```text
                USER
                  │
                  ▼
             Frontend UI
                  │
        ┌─────────┴─────────┐
        │                   │
        ▼                   ▼
   YouTube Chat        PDF Chat
        │                   │
        ▼                   ▼
YouTube Loader       PDF Loader
        │                   │
        └─────────┬─────────┘
                  ▼
             Raw Text
                  ▼
         Text Chunking
                  ▼
     HuggingFace Embeddings
                  ▼
        FAISS Vector Store
                  ▼
             Retriever
                  ▼
        Relevant Context
                  ▼
      Llama 3.3 70B (Groq)
                  ▼
          Final Response
```

---

# 🔄 Working Flow

```text
User Query
    │
    ▼
Load Source (PDF / YouTube)
    │
    ▼
Extract Text
    │
    ▼
Chunk Text
    │
    ▼
Generate Embeddings
    │
    ▼
Store in FAISS
    │
    ▼
Retrieve Relevant Chunks
    │
    ▼
Build Prompt
    │
    ▼
Llama 3.3 70B
    │
    ▼
Generate Answer
    │
    ▼
Return Response
```

---

# 📂 Project Structure

```text
Multi-Source-AI-Chatbot/
│
├── backend/
│   ├── llm/
│   │   └── llm_loader.py
│   │
│   ├── loaders/
│   │   ├── pdf_loader.py
│   │   └── youtube_loader.py
│   │
│   ├── rag/
│   │   ├── retriever.py
│   │   └── vector_store.py
│   │
│   ├── pipeline.py
│   └── main.py
│
├── data/
│   └── pdf/
│
├── frontend/
│
├── requirements.txt
└── README.md
```

---

# 🛠️ Technology Stack

### Programming Language

* Python

### Backend

* FastAPI

### Frontend

* Streamlit

### AI & RAG Framework

* LangChain

### Embedding Model

* all-MiniLM-L6-v2

### Vector Database

* FAISS

### Large Language Model

* Llama 3.3 70B Versatile

### Inference Provider

* Groq

### Data Sources

* PDF Documents
* YouTube Video Transcripts

---

# 🧩 Core Components

## 1. PDF Loader

Extracts text from uploaded PDF files using LangChain's PDF loader.

### Responsibilities

* Read PDF files
* Extract text content
* Clean extracted text
* Pass content to the RAG pipeline

---

## 2. YouTube Loader

Fetches and processes video transcripts using the YouTube Transcript API.

### Responsibilities

* Retrieve transcript
* Handle manual and auto-generated captions
* Convert transcript into searchable text

---

## 3. Text Chunking

Uses RecursiveCharacterTextSplitter.

### Configuration

* Chunk Size: 500
* Chunk Overlap: 100

### Benefits

* Preserves context
* Improves retrieval quality
* Reduces token usage

---

## 4. Embedding Generation

Uses the Hugging Face MiniLM embedding model.

### Purpose

Convert text chunks into vector representations that capture semantic meaning.

---

## 5. Vector Storage

Uses FAISS for efficient similarity search.

### Benefits

* Fast retrieval
* Scalable
* Lightweight
* Open-source

---

## 6. Retriever

Retrieves the most relevant chunks based on the user's query.

### Functionality

* Semantic search
* Duplicate filtering
* Context optimization

---

## 7. LLM Response Generation

Uses Llama 3.3 70B hosted on Groq.

### Responsibilities

* Understand retrieved context
* Generate grounded answers
* Follow strict response formatting rules

---

# ⚡ Performance Optimizations

## LLM Caching

```python
@lru_cache(maxsize=1)
```

Prevents repeated model initialization.

---

## Embedding Model Caching

```python
@lru_cache(maxsize=1)
```

Loads embedding model only once.

---

## Vector Database Caching

```python
@lru_cache(maxsize=5)
```

Reuses previously generated FAISS indexes.

---

# 📡 API Endpoints

## PDF Chat

```http
POST /chat/pdf
```

### Input

* PDF File
* Question
* Chat History (Optional)

### Output

* Generated Answer
* Source Chunks

---

## YouTube Chat

```http
POST /chat/youtube
```

### Input

* Video ID
* Question
* Chat History (Optional)

### Output

* Generated Answer
* Source Chunks

---

# 🚀 Installation Guide

## Clone Repository

```bash
git clone https://github.com/yourusername/multi-source-ai-chatbot.git

cd multi-source-ai-chatbot
```

---

## Create Virtual Environment

```bash
python -m venv venv
```

Activate:

```bash
venv\Scripts\activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Configure API Key

Create:

```python
config.py
```

Add:

```python
GROQ_API_KEY = "YOUR_GROQ_API_KEY"
```

---

## Run Backend

```bash
uvicorn backend.main:app --reload
```

---

## Run Frontend

```bash
streamlit run app.py
```

---

# 📊 Key Features

✅ Multi-Source Knowledge Retrieval

✅ Retrieval-Augmented Generation (RAG)

✅ PDF Question Answering

✅ YouTube Video Question Answering

✅ Context-Aware Conversations

✅ Semantic Search

✅ Fast Vector Retrieval

✅ Hallucination Reduction

✅ Source-Based Responses

✅ Scalable Architecture

---

# 🔮 Future Enhancements

* Multi-PDF Chat
* Research Paper Analysis
* Website Content Chat
* Audio File Support
* Persistent Vector Storage
* User Authentication
* Cloud Deployment
* Conversation Memory
* Citation-Based Responses
* Multi-Language Support

---

# 📚 Learning Outcomes

Through this project, I gained hands-on experience with:

* Retrieval-Augmented Generation (RAG)
* LangChain Framework
* Prompt Engineering
* Embedding Models
* Vector Databases (FAISS)
* FastAPI Development
* Streamlit Frontend Development
* LLM Integration
* Semantic Search Systems
* End-to-End AI Application Development

---

# 👨‍💻 Author

## Suman Kumar

B.Tech (Honors) – Computer Science & Engineering (Artificial Intelligence)

### Connect With Me

LinkedIn:
https://www.linkedin.com/in/suman-kumar-9754752ab/

GitHub:
https://github.com/SumanKumarUpadhyay

---

## ⭐ If you like this project, consider giving it a star!
