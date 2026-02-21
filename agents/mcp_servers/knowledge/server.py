"""Knowledge MCP Server — 3 tools: semantic search, graph query, store preference."""

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Knowledge", host="0.0.0.0", port=8005)


@mcp.tool()
def semantic_search_packages(
    query: str,
    destination: str | None = None,
    limit: int = 5,
) -> dict:
    """Search travel packages using semantic similarity.

    In production, this queries pgvector embeddings.
    Currently returns mock results.
    """
    mock_results = [
        {
            "title": "Tokyo Explorer: 5-Day Urban Adventure",
            "destination": "Japan",
            "similarity": 0.92,
            "slug": "tokyo-explorer-5day",
        },
        {
            "title": "Kyoto & Osaka Cultural Journey",
            "destination": "Japan",
            "similarity": 0.88,
            "slug": "kyoto-osaka-cultural-7day",
        },
        {
            "title": "Taipei City Break: 4 Days",
            "destination": "Taiwan",
            "similarity": 0.85,
            "slug": "taipei-city-break-4day",
        },
        {
            "title": "Hokkaido Winter Ski Paradise",
            "destination": "Japan",
            "similarity": 0.82,
            "slug": "hokkaido-ski-6day",
        },
        {
            "title": "Taiwan Night Market Food Trail",
            "destination": "Taiwan",
            "similarity": 0.80,
            "slug": "taiwan-night-market-food-5day",
        },
    ]

    results = mock_results
    if destination:
        results = [r for r in results if r["destination"].lower() == destination.lower()]

    return {
        "query": query,
        "destination_filter": destination,
        "results": results[:limit],
    }


@mcp.tool()
def query_knowledge_graph(query: str, group_id: str | None = None) -> dict:
    """Query the knowledge graph for travel-related information.

    In production, this queries the Graphiti (Neo4j) knowledge graph.
    Currently returns mock data.
    """
    return {
        "query": query,
        "group_id": group_id,
        "entities": [
            {
                "type": "destination",
                "name": "Tokyo",
                "properties": {"country": "Japan", "best_season": "spring"},
            },
            {
                "type": "activity",
                "name": "Cherry Blossom Viewing",
                "properties": {"season": "spring", "cost": "free"},
            },
        ],
        "relationships": [
            {"from": "Tokyo", "to": "Cherry Blossom Viewing", "type": "HAS_ACTIVITY"},
        ],
        "note": "Knowledge graph integration pending. Results are illustrative.",
    }


@mcp.tool()
def store_user_preference(
    user_id: str,
    preference_text: str,
    category: str,
) -> dict:
    """Store a user preference in the knowledge graph.

    Categories: food, accommodation, activities, transport, budget, style
    """
    return {
        "status": "stored",
        "user_id": user_id,
        "category": category,
        "preference": preference_text,
        "note": "Preference stored. Will be used for personalized recommendations.",
    }


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
