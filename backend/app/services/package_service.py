
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.exceptions import NotFoundError
from app.models.package import PackageDay, PackageTag, TravelPackage

# Fields that can be translated on each model
_PACKAGE_I18N_FIELDS = ("title", "summary", "description", "highlights")
_DAY_I18N_FIELDS = ("title", "description")
_TAG_I18N_FIELDS = ("tag",)


def _apply_locale(
    obj: TravelPackage | PackageDay | PackageTag,
    locale: str | None,
    fields: tuple[str, ...],
) -> None:
    """Overlay translated values onto a model instance (mutates in-place).

    If *locale* is None or "en", no-op (English is the base language).
    For any other locale, look up ``obj.translations[locale][field]`` and
    overwrite the base field when a translation exists.
    """
    if not locale or locale == "en":
        return
    translations = getattr(obj, "translations", None)
    if not translations or locale not in translations:
        return
    locale_data: dict = translations[locale]
    for field in fields:
        if field in locale_data:
            setattr(obj, field, locale_data[field])


async def list_packages(
    db: AsyncSession,
    destination: str | None = None,
    category: str | None = None,
    min_price: float | None = None,
    max_price: float | None = None,
    min_duration: int | None = None,
    max_duration: int | None = None,
    limit: int = 20,
    offset: int = 0,
    locale: str | None = None,
) -> list[TravelPackage]:
    stmt = select(TravelPackage).where(TravelPackage.is_published.is_(True))

    if destination:
        stmt = stmt.where(TravelPackage.destination == destination)
    if category:
        stmt = stmt.where(TravelPackage.category == category)
    if min_price is not None:
        stmt = stmt.where(TravelPackage.price_usd >= min_price)
    if max_price is not None:
        stmt = stmt.where(TravelPackage.price_usd <= max_price)
    if min_duration is not None:
        stmt = stmt.where(TravelPackage.duration_days >= min_duration)
    if max_duration is not None:
        stmt = stmt.where(TravelPackage.duration_days <= max_duration)

    stmt = stmt.order_by(TravelPackage.created_at.desc()).offset(offset).limit(limit)
    result = await db.execute(stmt)
    packages = list(result.scalars().all())
    for pkg in packages:
        _apply_locale(pkg, locale, _PACKAGE_I18N_FIELDS)
    return packages


async def get_package_by_slug(
    db: AsyncSession, slug: str, locale: str | None = None,
) -> TravelPackage:
    stmt = (
        select(TravelPackage)
        .where(TravelPackage.slug == slug)
        .options(selectinload(TravelPackage.days), selectinload(TravelPackage.tags))
    )
    result = await db.execute(stmt)
    package = result.scalar_one_or_none()
    if not package:
        raise NotFoundError("Package not found")
    _apply_locale(package, locale, _PACKAGE_I18N_FIELDS)
    for day in package.days:
        _apply_locale(day, locale, _DAY_I18N_FIELDS)
    for tag in package.tags:
        _apply_locale(tag, locale, _TAG_I18N_FIELDS)
    return package


async def get_categories(db: AsyncSession) -> list[str]:
    stmt = select(TravelPackage.category).distinct().where(TravelPackage.is_published.is_(True))
    result = await db.execute(stmt)
    return [row[0] for row in result.all()]


async def get_destinations(db: AsyncSession) -> list[str]:
    stmt = (
        select(TravelPackage.destination).distinct().where(TravelPackage.is_published.is_(True))
    )
    result = await db.execute(stmt)
    return [row[0] for row in result.all()]
