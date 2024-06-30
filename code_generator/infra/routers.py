import os

from base_request import EntityItem


def generate_routers(entity_name: str, plural_entity_name: str, items: list[EntityItem]) -> None:
    from code_generator.application.errors import generate_errors
    from code_generator.application.dtos import generate_dtos

    generate_errors(entity_name, items)
    generate_dtos(entity_name, items)

    model_name_min = entity_name
    model_name = f"{entity_name.capitalize()}"

    filename = f"src/infra/api/routers/{model_name_min}.py"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open("src/infra/api/routers/__init__.py", "a") as f:
        f.write(
            f"from src.infra.api.routers.{model_name_min} import router as router_{plural_entity_name}\n"
        )

    with open(filename, "w+") as f:
        f.write(
            f"""# -*- coding: utf-8 -*-
from typing import Tuple, Optional
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, status

from src.infra.models import get_db
from src.{model_name_min}.domain.entities import {model_name}
from src.{model_name_min}.application.dtos import Create{model_name}Input, Update{model_name}Input
from src.{model_name_min}.application.errors import {model_name}NotFound
from src.infra.repositories import {model_name_min} as {model_name_min}_repository

router = APIRouter()

@router.get("/{plural_entity_name}", tags=["{plural_entity_name}"])
async def find_{plural_entity_name}(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    {plural_entity_name}: Tuple[{model_name}] = {model_name_min}_repository.find_all(db, skip, limit)
    return {'{'}"{plural_entity_name}": {plural_entity_name}{'}'}


@router.get("/{plural_entity_name}/{'{'}{model_name_min}_id{'}'}", tags=["{plural_entity_name}"])
async def find_{model_name_min}({model_name_min}_id: str, db: Session = Depends(get_db)):
    {model_name_min}: Optional[{model_name}] = {model_name_min}_repository.find_by_id(db, {model_name_min}_id)
    if not {model_name_min}:
        return {model_name}NotFound()
    return {'{'}"{model_name_min}": {model_name_min}{'}'}


@router.post("/{plural_entity_name}", tags=["{plural_entity_name}"], status_code=status.HTTP_201_CREATED)
async def create_{model_name_min}({model_name_min}: Create{model_name}Input, db: Session = Depends(get_db)):
    {model_name_min}_created = {model_name_min}_repository.save(db, {model_name_min})
    return {'{'}"{model_name_min}": {model_name_min}_created{'}'}


@router.patch("/{plural_entity_name}", tags=["{plural_entity_name}"])
async def update_{model_name_min}(input: Update{model_name}Input, db: Session = Depends(get_db)):
    {model_name_min}: Optional[{model_name}] = {model_name_min}_repository.find_by_id(db, input.id)
    if not {model_name_min}:
        return {model_name}NotFound()

    updated_{model_name_min} = {model_name_min}_repository.update(db, input)
    return {'{'}"message": "updated", "{model_name_min}": updated_{model_name_min}{'}'}


@router.delete("/{plural_entity_name}/{'{'}{model_name_min}_id{'}'}", tags=["{plural_entity_name}"])
async def delete_{model_name_min}(
    {model_name_min}_id: str,
    db: Session = Depends(get_db)
):
    {model_name_min}: Optional[{model_name}] = {model_name_min}_repository.find_by_id(db, {model_name_min}_id)
    if not {model_name_min}:
        return {model_name}NotFound()

    {model_name_min}_repository.delete(db, {model_name_min}_id)
    return {'{'}"message": "deleted"{'}'}
"""
        )
