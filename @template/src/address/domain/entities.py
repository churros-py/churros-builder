# -*- coding: utf-8 -*-
from __future__ import annotations  # Needed for forward references in type hints
from typing import Optional
from datetime import datetime, timezone
from dataclasses import dataclass, field

from src.__seedwork.domain.entities import Entity


@dataclass(kw_only=True, frozen=True, slots=True)
class Address(Entity):
    id: int
    street: str
    user: 'User' = field(init=False)  # type: ignore

    def __post_init__(self):
        if not self.created_at:
            self._set('created_at',  datetime.now(
                timezone.utc))
        self.user.address = self  # Set the reverse reference
