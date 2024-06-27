
# -*- coding: utf-8 -*-
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.infra.models import Base
from src.user.domain.entities import User


class ProductModel(Base):
    __tablename__ = "products"

    id: str = Column(String(255), primary_key=True, index=True)
    name: str = Column(String(255))
    expiration_date: datetime = Column(DateTime())
    quantity: int = Column(Integer())
    weight: float = Column(Float())
    description: str = Column(String(255))
    active: bool = Column(Boolean())
    user_id = Column(Integer, ForeignKey('users.id'))
    user = relationship('UserModel', back_populates='products')
    created_at: datetime = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )
