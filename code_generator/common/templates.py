template_model = """
# -*- coding: utf-8 -*-
from dotenv import dotenv_values
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

envs = dotenv_values(".env")
engine = create_engine(envs["DATABASE_URL"])
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
"""

template_schema = """
# -*- coding: utf-8 -*-
from __future__ import annotations
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy import Column, String, Boolean, DateTime, Float, Integer, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

from src.infra.models import Base
"""

timestamp_model = """
    created_at: datetime = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: datetime = Column(
        DateTime(timezone=True),
        onupdate=func.now(),
    )
"""


imports_entity = """# -*- coding: utf-8 -*-
from __future__ import annotations
from typing import Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field\n"""


imports_repository = """
# -*- coding: utf-8 -*-
import json
from typing import List
from sqlalchemy.orm import Session, Query
"""
