import uuid

import httpx
from pgvector.sqlalchemy import Vector
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.models.embedding import TravelEmbedding


async def generate_embedding(text_content: str) -> list[float]:
    """Generate embedding using OpenRouter / OpenAI-compatible API."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(
            f"{settings.openrouter_base_url}/embeddings",
            headers={"Authorization": f"Bearer {settings.openrouter_api_key}"},
            json={
                "model": "openai/text-embedding-3-small",
                "input": text_content,
            },
            timeout=30.0,
        )
        data = resp.json()
        return data["data"][0]["embedding"]


async def store_embedding(
    db: AsyncSession,
    source_type: str,
    source_id: uuid.UUID,
    content_text: str,
    embedding: list[float],
) -> TravelEmbedding:
    record = TravelEmbedding(
        source_type=source_type,
        source_id=source_id,
        content_text=content_text,
        embedding=embedding,
    )
    db.add(record)
    await db.commit()
    await db.refresh(record)
    return record


async def semantic_search(
    db: AsyncSession,
    query_embedding: list[float],
    source_type: str | None = None,
    limit: int = 10,
) -> list[dict]:
    """Cosine similarity search via pgvector."""
    embedding_str = "[" + ",".join(str(x) for x in query_embedding) + "]"

    where_clause = ""
    if source_type:
        where_clause = f"AND source_type = '{source_type}'"

    sql = text(f"""
        SELECT id, source_type, source_id, content_text,
               1 - (embedding <=> :embedding::vector) AS similarity
        FROM travel_embeddings
        WHERE embedding IS NOT NULL {where_clause}
        ORDER BY embedding <=> :embedding::vector
        LIMIT :limit
    """)

    result = await db.execute(sql, {"embedding": embedding_str, "limit": limit})
    rows = result.fetchall()

    return [
        {
            "id": str(row.id),
            "source_type": row.source_type,
            "source_id": str(row.source_id),
            "content_text": row.content_text,
            "similarity": float(row.similarity),
        }
        for row in rows
    ]
