"""
StockRAG - Modular RAG system for NYSE company information.

Quick Start:
    from stockrag import create_context, load_annual_reports, build_index, query

    ctx = create_context("AAPL", "Apple Inc.")
    load_annual_reports(ctx, ["./reports/2024.pdf"])
    build_index(ctx)
    response = query(ctx, "What was the revenue?")
"""

# Version
__version__ = "0.1.0"

# Context and configuration
from stockrag.core.context import RAGContext
from stockrag.core.config import (
    RAGConfig,
    LLMConfig,
    EmbeddingConfig,
    ChunkingConfig,
    VectorStoreConfig,
)

# Context factory
from stockrag.client import create_context

# Functional API - Loaders
from stockrag.loaders import (
    load_sec_filings,
    load_annual_reports,
    load_company_website,
    load_news_releases,
)

# Functional API - Index
from stockrag.index import build_index, load_existing_index

# Functional API - Query
from stockrag.query import create_query_engine, query, query_with_filters

# Functional API - Maintenance
from stockrag.maintenance import update_with_new_data, get_stats

# Custom exceptions
from stockrag.core.exceptions import (
    StockRAGError,
    NoDocumentsError,
    IndexNotBuiltError,
    ConfigurationError,
)

__all__ = [
    # Version
    "__version__",
    # Core
    "RAGContext",
    "RAGConfig",
    "LLMConfig",
    "EmbeddingConfig",
    "ChunkingConfig",
    "VectorStoreConfig",
    "create_context",
    # Loaders
    "load_sec_filings",
    "load_annual_reports",
    "load_company_website",
    "load_news_releases",
    # Index
    "build_index",
    "load_existing_index",
    # Query
    "create_query_engine",
    "query",
    "query_with_filters",
    # Maintenance
    "update_with_new_data",
    "get_stats",
    # Exceptions
    "StockRAGError",
    "NoDocumentsError",
    "IndexNotBuiltError",
    "ConfigurationError",
]
