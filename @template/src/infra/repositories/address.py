
# -*- coding: utf-8 -*-
import json
from typing import List
from sqlalchemy.orm import Session, Query

from src.address.application.dtos import CreateAddressInput, UpdateAddressInput
from src.address.domain.entities import Address
from src.infra.schemas.address import AddressModel


def to_entity(model: Query | AddressModel) -> Address | None:
    if not model:
        return

    return Address(
        model.street,
        model.user,
    )


def find_all(db: Session, skip: int = 0, limit: int = 100) -> List[Address]:
    addresss = (
        db.query(AddressModel).offset(skip).limit(limit)
    )
    return tuple(map(to_entity, addresss))


def find_by_id(db: Session, address_id: str) -> Address | None:
    address = (
        db.query(AddressModel)
        .filter(AddressModel.id == address_id)
        .first()
    )
    return to_entity(address)


def delete(db: Session, address_id: str) -> None:
    db.query(AddressModel).filter(AddressModel.id == address_id).delete()
    db.commit()


def save(db: Session, input: CreateAddressInput) -> Address | None:
    address = AddressModel(**json.loads(input.json()))
    db.add(address)
    db.commit()
    return to_entity(address)


def update(db: Session, input: UpdateAddressInput) -> Address | None:
    address_id = input.id
    data: dict = json.loads(input.json())
    data = {attribute: value for attribute, value in data.items() if value != None and attribute != 'id'}

    db.query(AddressModel).filter(AddressModel.id == address_id).update(
        data
    )
    db.commit()
    updated_address = db.query(AddressModel).filter(AddressModel.id == input.id).first()
    return to_entity(updated_address)
