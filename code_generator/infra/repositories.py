import os

from base_request import EntityItem
from code_generator.common.templates import imports_repository


def generate_repository(entity_name: str, plural_entity_name: str, entity_items: list[EntityItem]) -> None:
    filename = f"src/infra/repositories/{entity_name}.py"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    open("src/infra/repositories/__init__.py", "a").close()

    model_name = f"{entity_name.capitalize()}"

    with open(filename, "w+") as f:
        f.write(imports_repository)

        f.write(
            f"""
from src.{entity_name}.application.dtos import Create{model_name}Input, Update{model_name}Input
from src.{entity_name}.domain.entities import {model_name}
from src.infra.schemas.{entity_name} import {model_name}Model
"""
        )

        f.write(
            f"""\n
def to_entity(model: Query | {model_name}Model) -> {model_name} | None:
    if not model:
        return

    return {model_name}(\n"""
        )

        for attribute in entity_items:
            field = attribute.name

            f.write(f"""        model.{field},\n""")
        f.write(
            f"""    )\n\n
def find_all(db: Session, skip: int = 0, limit: int = 100) -> List[{model_name}]:
    {plural_entity_name} = (
        db.query({model_name}Model).offset(skip).limit(limit)
    )
    return tuple(map(to_entity, {plural_entity_name}))


def find_by_id(db: Session, {entity_name}_id: str) -> {model_name} | None:
    {entity_name} = (
        db.query({model_name}Model)
        .filter({model_name}Model.id == {entity_name}_id)
        .first()
    )
    return to_entity({entity_name})


def delete(db: Session, {entity_name}_id: str) -> None:
    db.query({model_name}Model).filter({model_name}Model.id == {entity_name}_id).delete()
    db.commit()


def save(db: Session, input: Create{model_name}Input) -> {model_name} | None:
    {entity_name} = {model_name}Model(**json.loads(input.json()))
    db.add({entity_name})
    db.commit()
    return to_entity({entity_name})


def update(db: Session, input: Update{model_name}Input) -> {model_name} | None:
    {entity_name}_id = input.id
    data: dict = json.loads(input.json())
    data = {'{'}attribute: value for attribute, value in data.items() if value != None and attribute != 'id'{'}'}

    db.query({model_name}Model).filter({model_name}Model.id == {entity_name}_id).update(
        data
    )
    db.commit()
    updated_{entity_name} = db.query({model_name}Model).filter({model_name}Model.id == input.id).first()
    return to_entity(updated_{entity_name})
"""
        )
