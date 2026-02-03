"""
RAG Knowledge Base for NYSE Company - Example Usage

This file demonstrates how to use the stockrag package.
"""

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from stockrag import (
    create_context,
    load_annual_reports,
    build_index,
    query,
    RAGConfig,
    LLMConfig,
)


def main():
    """Example using the functional API."""
    # Custom configuration (optional)
    config = RAGConfig(
        llm=LLMConfig(
            model="llama-3.3-70b-versatile",
            temperature=0.1,
        )
    )

    # Create context
    ctx = create_context("AAPL", "Apple Inc.", config)

    # Load data from various sources
    # from stockrag import load_sec_filings, load_company_website, load_news_releases
    # load_sec_filings(ctx, filing_types=["10-K", "10-Q"])
    load_annual_reports(ctx, ["./data/apple_annual_report_2024.pdf"])
    # load_company_website(ctx, urls=[
    #     "https://www.apple.com/investor-relations/",
    #     "https://www.apple.com/newsroom/"
    # ])
    # load_news_releases(ctx, news_urls=[
    #     "https://www.apple.com/newsroom/2024/01/apple-reports-first-quarter-results/"
    # ])

    # Build index
    build_index(ctx)

    # Or load existing index
    # from stockrag import load_existing_index
    # load_existing_index(ctx)

    # Query examples
    response = query(ctx, "What was the revenue in the last fiscal year?")
    print(f"\nAnswer: {response}")

    response = query(ctx, "What are the main business segments?")
    print(f"\nAnswer: {response}")

    # Query with filters
    # from stockrag import query_with_filters
    # response = query_with_filters(
    #     ctx,
    #     "What were the key highlights?",
    #     source_filter="Annual Report"
    # )

    # Get statistics
    # from stockrag import get_stats
    # stats = get_stats(ctx)
    # print(f"\nKnowledge Base Stats: {stats}")

    print("\nRAG system initialized with Groq LLM and open source embeddings.")


if __name__ == "__main__":
    main()
