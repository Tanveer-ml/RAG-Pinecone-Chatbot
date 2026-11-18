
# RAG Pinecone Chatbot

An AI-powered company chatbot built using
Retrieval Augmented Generation (RAG).

## Technologies Used
- Python
- OpenAI API
- Pinecone Vector Database
- Streamlit
- Vector Embeddings

## Features
- Document ingestion
- Text embeddings
- Vector storage using Pinecone
- Semantic search
- Context-based AI responses
- Interactive Streamlit interface

## Installation

Install dependencies:

pip install -r requirements.txt

Create a .env file containing:

OPENAI_API_KEY=your_api_key
PINECONE_API_KEY=your_api_key

Run document ingestion:

python ingest.py

Run the application:

python -m streamlit run app.py

## Author
Tanveer Ul Salam
