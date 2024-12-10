---
# 🌟 LLAMA-LEX APP 🌟  
🚀 **Real-Time Document Interaction System Using RAG and LLAMA 3.2**

## Overview
**LLAMA-LEX APP** is an innovative application designed to revolutionize document interaction. By leveraging advanced AI models, users can upload, summarize, and chat with documents in real time. The system is built using **LLAMA 3.2**, **BGE Embeddings**, and **Qdrant** for efficient document search and retrieval, running in a **Docker** container for seamless deployment.

## Key Features
- **Upload Documents:** Effortlessly upload PDF documents for real-time processing.
- **Summarize:** Quickly generate concise summaries for faster document understanding.
- **Chat:** Engage in intelligent, interactive conversations with your documents through our chatbot.

## Built Using
- **LLAMA 3.2 (3B):** An advanced Large Language Model for document comprehension.
- **BGE Embeddings:** For high-quality text embeddings, improving document search and understanding.
- **Qdrant:** A vector database for fast and efficient similarity searches.
- **Docker:** Used to containerize the application for portability and ease of deployment.

## Prerequisites

Before you can run LLAMA-LEX, ensure you have the following installed on your system:

- Docker ([Installation guide](https://docs.docker.com/get-docker/))
- Python 3.8+ (Optional for non-containerized use)
  
## Getting Started

### 1. Clone the repository:
```bash
git clone https://github.com/nikhil80520/LLAMA-LEX.git
cd LLAMA-LEX
```

### 2. Set up the Docker Environment:
You can build and run the project using Docker. The container will include the necessary dependencies (LLAMA 3.2, Qdrant, and BGE embeddings).

```bash
# Build the Docker container
docker build -t llama-lex-app .

# Run the Docker container
docker run -p 8000:8000 llama-lex-app
```

### 3. Access the Application:
Once the Docker container is running, open your web browser and go to:
```
http://localhost:8000
```

From here, you can upload documents, get summaries, and chat with your documents!
