# OmniContext POC

An AI-powered Repository Intelligence and Knowledge Retrieval Platform built using GitHub MCP, Atlassian MCP, Hybrid RAG, Knowledge Graphs, Neo4j, FAISS, and Vertex AI Gemini.

---

## Overview

OmniContext enables intelligent repository and knowledge discovery by combining:

- GitHub MCP integration
- Atlassian MCP integration
- Hybrid RAG retrieval
- Knowledge Graph generation
- Neo4j graph database
- Semantic search using FAISS
- AI-powered question answering using Vertex AI Gemini

The platform transforms repository metadata into a graph structure and combines graph-based retrieval with vector-based retrieval to provide context-aware, relationship-aware answers.

---

## Key Features

### GitHub MCP Integration

- Connect to GitHub Remote MCP
- Retrieve repositories, commits, branches, and pull requests
- Repository metadata extraction
- Dynamic repository intelligence

### Atlassian MCP Integration

- Jira issue retrieval
- Project knowledge discovery
- Enterprise knowledge integration

### Hybrid RAG

- Document chunking and indexing
- Semantic similarity search
- FAISS-based retrieval
- Context-aware question answering

### Graph Schema Design

Dynamic knowledge graph generation from GitHub data.

#### Entities

- Repository
- Branch
- Commit
- Contributor

#### Relationships

- HAS_COMMIT
- HAS_BRANCH
- AUTHORED
- HEAD_COMMIT

### Graph Retrieval

Supports graph traversal and graph-based question answering.

Sample Graph Questions:

```text
Who made the latest changes?

What is the head commit of main?

Show all commits by Sanket-More-Xoriant.
```

### Neo4j Integration

- Graph persistence in Neo4j
- Cypher query support
- Graph visualization
- Relationship exploration
- Graph-based retrieval workflows

### Repository Analysis

- Repository overview generation
- Architecture analysis
- Module discovery
- Specification generation
- Engineering insights

---

## Architecture

```text
                    User Question
                           │
                           ▼
                   Question Router
                      /        \
                     /          \
                    ▼            ▼

             Graph Retrieval   Vector Retrieval
                 (Neo4j)          (FAISS)

                    \            /
                     \          /
                      ▼        ▼

                   Combined Context
                           │
                           ▼
                   Vertex AI Gemini
                           │
                           ▼
                     Final Answer
```

---

## Knowledge Graph Architecture

```text
GitHub MCP
     │
     ▼

Repository
 ├── HAS_BRANCH ───► Branch
 ├── HAS_COMMIT ───► Commit
 │
Contributor
 └── AUTHORED ────► Commit

Branch
 └── HEAD_COMMIT ─► Commit
```

---

## Neo4j Graph Integration

The generated GitHub knowledge graph is persisted into Neo4j and can be queried using Cypher.

Example Query:

```cypher
MATCH (n)-[r]->(m)
RETURN n,r,m
```

Example Output:

```text
Repository
  ├─ HAS_BRANCH ─► main
  ├─ HAS_COMMIT ─► f5aa180

Contributor
  └─ AUTHORED ─► f5aa180

main
  └─ HEAD_COMMIT ─► f5aa180
```

---

## Tech Stack

- Python
- GitHub MCP
- Atlassian MCP
- Neo4j
- FAISS
- Vertex AI Gemini
- Scikit-Learn
- AsyncIO

---

## Project Structure

```text
omnicontext-poc/
│
├── agents/
│   ├── github_graph_agent.py
│   ├── graph_retrieval_agent.py
│   ├── neo4j_graph_loader.py
│   └── ...
│
├── connectors/
│   ├── github_mcp_client.py
│   ├── neo4j_connector.py
│   └── ...
│
├── data/
├── llm/
│
├── app.py
├── requirements.txt
├── test_graph_retrieval.py
├── test_graph_qa.py
├── test_neo4j_connection.py
├── test_neo4j_load.py
└── README.md
```

---

## Setup

### Clone Repository

```bash
git clone https://github.com/Sanket-More-Xoriant/omnicontext-poc.git
```

### Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

```bash
venv\Scripts\activate
```

### Install Dependencies

```bash
python -m pip install -r requirements.txt
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

---

## Neo4j Setup

Install Neo4j Desktop.

Create Local Instance:

```text
Instance Name:
omnicontext-graph

User:
neo4j

Password:
********
```

Start the database.

Verify connection:

```bash
python test_neo4j_connection.py
```

Expected Output:

```text
Neo4j Connected
```

---

## Running Graph Features

### Build GitHub Graph

```bash
python test_mcp_graph.py
```

### Test Graph Retrieval

```bash
python test_graph_retrieval.py
```

### Test Natural Language Graph QA

```bash
python test_graph_qa.py
```

### Load Graph Into Neo4j

```bash
python test_neo4j_load.py
```

---

## Example Graph Questions

```text
Who made the latest changes?

What is the head commit of main?

Show all commits authored by Sanket-More-Xoriant.

What is the latest commit in the repository?
```

Example Response:

```json
{
  "author": "Sanket-More-Xoriant",
  "commit": "f5aa180"
}
```

---

## Current Capabilities

✅ GitHub MCP Integration

✅ Atlassian MCP Integration

✅ Repository Analysis

✅ Hybrid RAG

✅ FAISS Semantic Search

✅ Knowledge Graph Generation

✅ Graph Retrieval Agent

✅ Natural Language Graph Queries

✅ Neo4j Integration

✅ Cypher-Based Graph Exploration

---

## Roadmap

- Neo4j-based Graph Retrieval
- Graph RAG
- Hybrid RAG + Graph RAG
- Multi-MCP Knowledge Graph
- Jira Graph Integration
- Repository Dependency Graph
- End-to-End Intelligent Knowledge Assistant

---

## Author

Sanket More

Software Engineer | AI Engineering | MCP | RAG | Knowledge Graphs | Neo4j
