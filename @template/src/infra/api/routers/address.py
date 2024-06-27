# -*- coding: utf-8 -*-
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from src.infra.models import get_db
from src.address.domain.entities import Address
from src.address.application.dtos import CreateAddressInput, UpdateAddressInput
from src.address.application.errors import AddressNotFound
from src.infra.repositories import address as address_repository

router = APIRouter()

@router.get("/addresss", tags=["addresss"])
async def find_addresss(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    addresss: Tuple[Address] = address_repository.find_all(db, skip, limit)
    return {"addresss": addresss}


@router.get("/addresss/{address_id}", tags=["addresss"])
async def find_address(address_id: str, db: Session = Depends(get_db)):
    address: Optional[Address] = address_repository.find_by_id(db, address_id)
    if not address:
        return AddressNotFound()
    return {"address": address}


@router.post("/addresss", tags=["addresss"], status_code=status.HTTP_201_CREATED)
async def create_address(address: CreateAddressInput, db: Session = Depends(get_db)):
    address_created = address_repository.save(db, address)
    return {"address": address_created}


@router.patch("/addresss", tags=["addresss"])
async def update_address(input: UpdateAddressInput, db: Session = Depends(get_db)):
    address: Optional[Address] = address_repository.find_by_id(db, input.id)
    if not address:
        return AddressNotFound()

    updated_address = address_repository.update(db, input)
    return {"message": "updated", "address": updated_address}


@router.delete("/addresss/{address_id}", tags=["addresss"])
async def delete_address(
    address_id: str,
    db: Session = Depends(get_db)
):
    address: Optional[Address] = address_repository.find_by_id(db, address_id)
    if not address:
        return AddressNotFound()

    address_repository.delete(db, address_id)
    return {"message": "deleted"}
