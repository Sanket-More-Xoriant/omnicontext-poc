class SpecificationAnalysisAgent:

    def analyze(
        self,
        repository_context="",
        architecture_context=""
    ):

        specification = f"""
========================
SYSTEM SPECIFICATION
========================

Project Purpose:
AI-powered Repository Intelligence Platform

Core Capabilities:
- Repository Analysis
- Architecture Analysis
- Commit Intelligence
- Pull Request Intelligence
- Hybrid RAG
- Omni Context Retrieval

Repository Summary:

{repository_context[:3000]}

Architecture Summary:

{architecture_context[:1500]}

Expected Use Cases:

- Repository Understanding
- Architecture Discovery
- Development Trend Analysis
- Commit Investigation
- PR Investigation
- Knowledge Retrieval

System Goal:

Provide comprehensive repository intelligence
using multiple context sources.
"""

        return specification