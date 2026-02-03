# StockRAG - Claude Code Guide

## Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Configure environment
echo "GROQ_API_KEY=your_key_here" > .env

# Run example
python main.py
```

## Architecture Overview

**StockRAG** is a modular RAG (Retrieval-Augmented Generation) system for financial document analysis, built on LlamaIndex. Uses a functional design with explicit context passing.

### Module Flow

```
loaders/ → index/ → query/ → maintenance/
   ↓         ↓        ↓           ↓
     All operate on RAGContext
```

### Core Pattern: Context-Driven Design

**RAGContext** (core/context.py:16) is a dataclass containing all shared state:
- Documents, index, query engine
- Vector store, storage context
- Chroma client/collection

Functions accept `ctx: RAGContext` as first parameter, avoiding global state.

### Configuration System

Nested dataclasses in core/config.py:
- `RAGConfig` → `LLMConfig`, `EmbeddingConfig`, `ChunkingConfig`, `VectorStoreConfig`
- Defaults auto-load from environment (`GROQ_API_KEY`)
- Custom configs passed to `create_context()`

## Technology Stack

- **LlamaIndex**: RAG orchestration framework (NOT custom implementation)
- **Groq API**: Remote LLM (llama-3.3-70b-versatile default)
- **HuggingFace**: Local embeddings (BAAI/bge-small-en-v1.5 default)
- **ChromaDB**: Persistent vector storage (local, per-ticker directories)

## Key Files

| File | Purpose |
|------|---------|
| `stockrag/client.py` | create_context factory function |
| `stockrag/core/context.py` | RAGContext dataclass |
| `stockrag/core/config.py` | Configuration dataclasses |
| `main.py` | Working example using functional API |
| `stockrag/loaders/` | Data ingestion (SEC, PDFs, web, news) |
| `stockrag/index/` | Index building/loading |
| `stockrag/query/` | Query engine + filtering |
| `stockrag/maintenance/` | Updates + statistics |

## Critical Details

### Vector Storage
- Path: `./chroma_db_{TICKER}/` (auto-created per ticker)
- Collection: `{TICKER}_knowledge_base`
- Persistent between runs

### LlamaIndex Global Settings
Configured in `client.py:_initialize_context()` (46-84):
- `Settings.llm` - Groq instance
- `Settings.embed_model` - HuggingFace embeddings
- `Settings.node_parser` - SentenceSplitter (chunk_size=1024, overlap=200)

### SEC Filings Loader
**Placeholder only** (loaders/sec.py) - Not implemented, raises NotImplementedError

### Example Usage

```python
from stockrag import create_context, load_annual_reports, build_index, query

ctx = create_context("AAPL", "Apple Inc.")
load_annual_reports(ctx, ["./data/report.pdf"])
build_index(ctx)
answer = query(ctx, "What was the revenue?")
```

## Environment Setup

Required:

```bash
GROQ_API_KEY=gsk_...
```

Optional overrides via RAGConfig:

- LLM model/temperature
- Embedding model
- Chunk size/overlap
- Vector store path/collection

## Architecture Notes

- **Stateless functions**: All state lives in RAGContext, passed explicitly
- **No global singletons**: Multiple RAGContext instances can coexist
- **LlamaIndex dependency**: Heavy reliance on LlamaIndex abstractions (Document, VectorStoreIndex, QueryEngine)
- **Local embeddings**: No API calls for embedding generation (cost optimization)
- **Persistent storage**: Vector DB survives process restarts via ChromaDB
