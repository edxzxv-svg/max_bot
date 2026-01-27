from datetime import datetime
from typing import Any
from uuid import UUID

from sqlalchemy import ARRAY, MetaData, func, types
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

metadata_obj = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)


class Base(DeclarativeBase):
    __abstract__ = True

    metadata = metadata_obj

    type_annotation_map = {
        list[UUID]: ARRAY(types.UUID),
        list[str]: ARRAY(types.String),
        dict[str, Any]: JSONB,
        int: types.BigInteger,
    }

    created_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(),
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.current_timestamp(),
        onupdate=func.current_timestamp(),
    )
