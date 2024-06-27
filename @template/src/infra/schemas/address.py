# -*- coding: utf-8 -*-
from __future__ import annotations  # Needed for forward references in type hints
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column, String, DateTime, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.infra.models import Base

class AddressModel(Base):
    __tablename__ = "addresses"

    id: str = Column(String(255), primary_key=True, index=True)
    street: str = Column(String(255))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["UserModel"] = relationship(back_populates="address") # type: ignore
    created_at: datetime = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )
