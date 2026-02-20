"""Initialize Graphiti indices in Neo4j."""

import asyncio
import os

from neo4j import AsyncGraphDatabase


async def init_graphiti():
    uri = os.getenv("NEO4J_URI", "bolt://trip-neo4j:7687")
    user = os.getenv("NEO4J_USER", "neo4j")
    password = os.getenv("NEO4J_PASSWORD", "tripneo4j")

    driver = AsyncGraphDatabase.driver(uri, auth=(user, password))

    async with driver.session() as session:
        # Create indices for Graphiti entities
        await session.run(
            "CREATE INDEX IF NOT EXISTS FOR (n:Entity) ON (n.name)"
        )
        await session.run(
            "CREATE INDEX IF NOT EXISTS FOR (n:Entity) ON (n.group_id)"
        )
        await session.run(
            "CREATE INDEX IF NOT EXISTS FOR (n:Episode) ON (n.created_at)"
        )
        print("Graphiti indices created successfully!")

    await driver.close()


if __name__ == "__main__":
    asyncio.run(init_graphiti())
