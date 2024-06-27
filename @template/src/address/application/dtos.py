# -*- coding: utf-8 -*-
from __future__ import annotations  # Needed for forward references in type hints
from pydantic import BaseModel

class Address(BaseModel):
    id: int
    street: str
    user: 'User' # type: ignore


class CreateAddressInput(BaseModel):
    id: int
    street: str
    user: 'User' # type: ignore


class UpdateAddressInput(BaseModel):
    street: str
    user: 'User' # type: ignore
