"""Knowledge graph service using Graphiti (Neo4j).

Provides user preference storage and retrieval for personalized recommendations.
"""

import logging

logger = logging.getLogger(__name__)

# Placeholder for Graphiti integration
# Will be connected to Neo4j in Phase 5


async def store_preference(user_id: str, preference_text: str, category: str) -> dict:
    """Store a user preference in the knowledge graph."""
    logger.info("Storing preference for user %s: %s", user_id, category)
    return {"status": "stored", "user_id": user_id, "category": category}


async def query_preferences(user_id: str, query: str) -> list[dict]:
    """Query user preferences from the knowledge graph."""
    logger.info("Querying preferences for user %s: %s", user_id, query)
    return []


async def query_knowledge(query: str, group_id: str | None = None) -> list[dict]:
    """Query the knowledge graph for travel information."""
    logger.info("Querying knowledge graph: %s", query)
    return []
