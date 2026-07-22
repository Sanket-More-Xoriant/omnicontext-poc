# Retrosync POC

GitHub Repository Intelligence Platform built using GitHub Remote MCP, FAISS, RAG, and Vertex AI Gemini.

## Overview

This project demonstrates end-to-end repository analysis using the GitHub Remote MCP Server.

The application can:

- Connect to GitHub Remote MCP Server
- Retrieve repository contents
- Build a repository cache
- Generate embeddings and perform semantic search
- Answer repository-specific questions
- Generate repository overviews
- Analyze commits and pull requests
- Generate repository specifications
- Provide source citations for answers

---

## Architecture

```text
GitHub Remote MCP
        ↓
Repository Cache
        ↓
Chunking
        ↓
TF-IDF Embeddings
        ↓
FAISS
        ↓
Retrieval
        ↓
Vertex AI Gemini
        ↓
Repository Analysis & Q&A
```

---

## Features

### Repository Analysis
- Repository overview generation
- Repository architecture analysis
- Major module identification

### Semantic Repository Search
- Chunk-based indexing
- FAISS vector search
- Context-aware Q&A

### GitHub MCP Integration
- Repository content retrieval
- File discovery
- Repository intelligence

### Commit Analysis
- Recent development trends
- Feature analysis
- Bug fix analysis

### Pull Request Analysis
- PR trend analysis
- Engineering focus areas
- Architecture change insights

### Specification Generation
- Automated repository specifications
- Project summaries
- Architecture documentation

---

## Tech Stack

- Python
- GitHub Remote MCP Server
- FAISS
- Vertex AI Gemini
- Scikit-Learn
- AsyncIO

---

## Project Structure

```text
retrosync-poc/
│
├── agents/
├── connectors/
├── llm/
├── data/
│
├── app.py
├── requirements.txt
├── .env.example
└── README.md
```

---

## Setup

### Clone Repository

```bash
git clone https://github.com/Sanket-More-Xoriant/retrosync-poc.git
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment

Create:

```text
.env
```

using:

```text
.env.example
```

### Run

```bash
python app.py
```

---

## Sample Questions

```text
What are the major modules in this repository?

Explain repository architecture.

How does MCP work in this repository?

Analyze recent commits.

Analyze recent pull requests.

Explain Pinecone integration.
```

