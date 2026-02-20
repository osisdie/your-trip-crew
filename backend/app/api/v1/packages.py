from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_optional_user
from app.models.user import User
from app.schemas.package import PackageDetailRead, PackageFilterParams, PackageListRead
from app.services import package_service
from app.services.embedding_service import generate_embedding, semantic_search

router = APIRouter()


@router.get("", response_model=list[PackageListRead])
async def list_packages(
    destination: str | None = Query(None),
    category: str | None = Query(None),
    min_price: float | None = Query(None),
    max_price: float | None = Query(None),
    min_duration: int | None = Query(None),
    max_duration: int | None = Query(None),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    locale: str | None = Query(None, max_length=10),
    db: AsyncSession = Depends(get_db),
):
    packages = await package_service.list_packages(
        db,
        destination=destination,
        category=category,
        min_price=min_price,
        max_price=max_price,
        min_duration=min_duration,
        max_duration=max_duration,
        limit=limit,
        offset=offset,
        locale=locale,
    )
    return packages


@router.get("/categories")
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await package_service.get_categories(db)


@router.get("/destinations")
async def get_destinations(db: AsyncSession = Depends(get_db)):
    return await package_service.get_destinations(db)


@router.get("/search/semantic")
async def semantic_search_packages(
    q: str = Query(..., min_length=2),
    destination: str | None = Query(None),
    limit: int = Query(10, ge=1, le=50),
    db: AsyncSession = Depends(get_db),
):
    embedding = await generate_embedding(q)
    results = await semantic_search(db, embedding, source_type="package", limit=limit)
    return results


@router.get("/{slug}", response_model=PackageDetailRead)
async def get_package(
    slug: str,
    locale: str | None = Query(None, max_length=10),
    db: AsyncSession = Depends(get_db),
):
    return await package_service.get_package_by_slug(db, slug, locale=locale)
