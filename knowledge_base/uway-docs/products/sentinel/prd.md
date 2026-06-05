# AI-AML-SENTINEL: Product Requirements Document (PRD) v1.0

## 1. Executive Summary
AI-AML-SENTINEL is an intelligent compliance engine designed to augment traditional transaction monitoring systems. It uses Large Language Models (LLMs) to identify complex, non-linear financial crime patterns and provides actionable compliance advisory in real-time.

## 2. Problem Statement
Traditional AML systems rely on hardcoded rules (e.g., "if amount > $10,000, then flag"). These systems suffer from:
- High false positive rates.
- Inability to detect "grey area" risks or evolving money laundering typologies.
- Lag in adapting to new regulatory standards (SFC, MiCA, MAS).

## 3. Core Features
### 3.1 Semantic Risk Analysis (AI-Core)
- **Typology Mapping**: Automate the identification of patterns like "Layering" and "Integration" by analyzing transaction narratives and metadata.
- **Contextual Scoring**: Assign risk scores based on the "intent" and "structure" of transactions, not just thresholds.

### 3.2 Regulatory Intelligence Integration
- **Dynamic Benchmarking**: Automatically update internal risk parameters against the latest SFC VATP guidelines and MiCA CASP requirements.
- **Audit-Ready Justification**: Generate human-readable explanations for every flag to assist compliance officers during regulatory audits.

### 3.3 Multi-License Support
- Unified monitoring for entities holding both crypto (VASP) and fiat (Payment) licenses.

## 4. Technical Architecture (High-Level)
- **API Layer**: FastAPI for high-speed transaction ingestion.
- **Intelligence Layer**: Google Gemini 1.5 Pro / Flash for semantic analysis.
- **Data Layer**: Vector database (e.g., Pinecone/Chroma) for storing regulatory knowledge and historical patterns.

## 5. Target Users
- Licensed VATPs in Hong Kong.
- CASPs in the European Union.
- Cross-border payment processors.

---
**Status**: Draft - 2026-04-24
**Owner**: Louie / UWAY Innovation Limited
