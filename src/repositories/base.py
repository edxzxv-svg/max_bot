from collections.abc import Iterable
from typing import Any, Generic, TypeVar, cast

from sqlalchemy import RowMapping, select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models import Base

T = TypeVar("T", bound=Base)


class BaseRepository(Generic[T]):
    def __init__(self, model: type[T]) -> None:
        self.model = model

    async def get_by(self, session: AsyncSession, **kwargs: Any) -> T | None:
        stmt = select(self.model).filter_by(**kwargs)
        instance = await session.execute(stmt)
        return instance.scalar()

    async def select(
        self, session: AsyncSession, **kwargs: Any
    ) -> list[T | dict[str, Any]]:
        fields_to_select = kwargs.pop("fields", None)
        exclude_fields = kwargs.pop("exclude_fields", [])

        if fields_to_select:
            selected_fields = [
                getattr(self.model, field) for field in fields_to_select
            ]
        else:
            selected_fields = [
                field
                for field in self.model.__table__.columns
                if not exclude_fields or field.name not in exclude_fields
            ]

        stmt = select(*selected_fields)

        if "offset" in kwargs:
            stmt = stmt.offset(kwargs.pop("offset"))

        if "limit" in kwargs:
            stmt = stmt.limit(kwargs.pop("limit"))

        instances = await session.execute(stmt.filter_by(**kwargs))
        result = instances.mappings().all()
        converted_result: list[T | dict[str, Any]] = []
        for item in result:
            if hasattr(item, "items") and isinstance(item, RowMapping):
                converted_result.append(dict(item))
            else:
                converted_result.append(cast(T, item))
        return converted_result

    async def get_all(
        self, session: AsyncSession, **kwargs: Any
    ) -> Iterable[T | dict[str, Any]]:
        stmt = select(self.model)
        instances = await session.execute(stmt.filter_by(**kwargs))
        return instances.scalars().all()

    async def create(self, session: AsyncSession, **kwargs: Any) -> T:
        instance = self.model(**kwargs)
        session.add(instance)
        await session.commit()
        return instance

    async def update(
        self, session: AsyncSession, instance: T, **kwargs: Any
    ) -> T:
        for key, value in kwargs.items():
            setattr(instance, key, value)
            session.add(instance)
        return instance
