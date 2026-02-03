"""
StockRAG client - Context factory for the RAG system.

Provides the create_context factory function to initialize RAGContext
with all necessary LlamaIndex settings and vector store configuration.
"""

import os
from typing import Optional

from llama_index.core import Settings, StorageContext
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.groq import Groq
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

from stockrag.core.context import RAGContext
from stockrag.core.config import RAGConfig
from stockrag.core.exceptions import ConfigurationError


def create_context(
    ticker: str,
    company_name: str,
    config: Optional[RAGConfig] = None,
) -> RAGContext:
    """
    Factory function to create and initialize a RAGContext.

    Args:
        ticker: Company stock ticker
        company_name: Full company name
        config: Optional RAGConfig (uses defaults if None)

    Returns:
        Initialized RAGContext with vector store configured
    """
    config = config or RAGConfig()
    ctx = RAGContext(ticker=ticker, company_name=company_name)
    _initialize_context(ctx, config)
    return ctx


def _initialize_context(ctx: RAGContext, config: RAGConfig) -> None:
    """Initialize LlamaIndex settings and vector store."""
    # Validate API key
    api_key = config.llm.api_key or os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise ConfigurationError(
            "Groq API key must be provided or set in GROQ_API_KEY environment variable"
        )

    # Configure LLM
    Settings.llm = Groq(
        model=config.llm.model,
        temperature=config.llm.temperature,
        api_key=api_key,
    )

    # Configure embeddings
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=config.embedding.model_name
    )

    # Configure chunking
    Settings.node_parser = SentenceSplitter(
        chunk_size=config.chunking.chunk_size,
        chunk_overlap=config.chunking.chunk_overlap,
    )

    # Initialize vector store
    persist_path = config.vector_store.persist_path or f"./chroma_db_{ctx.ticker}"
    collection_name = (
        config.vector_store.collection_name or f"{ctx.ticker}_knowledge_base"
    )

    ctx.chroma_client = chromadb.PersistentClient(path=persist_path)
    ctx.chroma_collection = ctx.chroma_client.get_or_create_collection(
        name=collection_name
    )
    ctx.vector_store = ChromaVectorStore(chroma_collection=ctx.chroma_collection)
    ctx.storage_context = StorageContext.from_defaults(vector_store=ctx.vector_store)
