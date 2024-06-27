
# -*- coding: utf-8 -*-
import json
from typing import List
from sqlalchemy.orm import Session, Query

from src.product.application.dtos import CreateProductInput, UpdateProductInput
from src.product.domain.entities import Product
from src.infra.schemas.product import ProductModel


def to_entity(model: Query | ProductModel) -> Product | None:
    if not model:
        return

    return Product(
        model.name,
        model.expiration_date,
        model.quantity,
        model.weight,
        model.description,
        model.active,
        model.user,
    )


def find_all(db: Session, skip: int = 0, limit: int = 100) -> List[Product]:
    products = (
        db.query(ProductModel).offset(skip).limit(limit)
    )
    return tuple(map(to_entity, products))


def find_by_id(db: Session, product_id: str) -> Product | None:
    product = (
        db.query(ProductModel)
        .filter(ProductModel.id == product_id)
        .first()
    )
    return to_entity(product)


def delete(db: Session, product_id: str) -> None:
    db.query(ProductModel).filter(ProductModel.id == product_id).delete()
    db.commit()


def save(db: Session, input: CreateProductInput) -> Product | None:
    product = ProductModel(**json.loads(input.json()))
    db.add(product)
    db.commit()
    return to_entity(product)


def update(db: Session, input: UpdateProductInput) -> Product | None:
    product_id = input.id
    data: dict = json.loads(input.json())
    data = {attribute: value for attribute, value in data.items() if value != None and attribute != 'id'}

    db.query(ProductModel).filter(ProductModel.id == product_id).update(
        data
    )
    db.commit()
    updated_product = db.query(ProductModel).filter(ProductModel.id == input.id).first()
    return to_entity(updated_product)
