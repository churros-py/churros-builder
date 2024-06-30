import os

from base_request import EntityItem, builtins_types, Relationship
from code_generator.common.templates import (
    timestamp_model,
    template_model,
    template_schema,
)


def convert_to_sqlalchemy_type(type: str) -> str:
    match type:
        case "str":
            return "String(255)"
        case "bool":
            return "Boolean()"
        case "int":
            return "Integer()"
        case "float":
            return "Float()"
        case "datetime":
            return "DateTime()"


models_filename = "src/infra/models.py"


def generate_model(entity_name: str, plural_entity_name: str, items: list[EntityItem]) -> None:
    if not os.path.exists(models_filename):
        os.makedirs(os.path.dirname(models_filename), exist_ok=True)
        open("src/infra/__init__.py", "a").close()
        with open(models_filename, "a+") as f:
            f.write(template_model)

    filename = f"src/infra/schemas/{entity_name}.py"

    if not os.path.exists(filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        open("src/infra/schemas/__init__.py", "a").close()
        with open(filename, "a+") as f:
            f.write(template_schema)

    with open(filename, "a+") as f:
        for attribute in items:
            type_of_field = attribute.type
            if type_of_field in builtins_types or type_of_field == "datetime":
                continue

            if attribute.type == "datetime":
                f.write(f"""from datetime import datetime\n""")
            elif attribute.relationship == Relationship.ONE_TO_ONE_PARENT:
                f.write(
                    f"""from src.infra.schemas.{attribute.type.lower()} import {attribute.type.capitalize()}Model\n"""
                )

        f.write(
            f"""\n\nclass {entity_name.capitalize()}Model(Base):
    __tablename__ = "{plural_entity_name}"

    id: str = Column(String(255), primary_key=True, index=True)"""
        )

        for attribute in items:
            field = attribute.name
            type_of_field = attribute.type

            if field in ("id", "created_at", "updated_at"):
                continue

            if convert_to_sqlalchemy_type(type_of_field) is None:
                if attribute.relationship == Relationship.MANY_TO_ONE:
                    f.write(
                        f"""
    {field}_id = Column(Integer, ForeignKey('{field}.id'))
    {field} = relationship('{field.capitalize()}Model', back_populates='{plural_entity_name}')"""
                    )
                elif attribute.relationship == Relationship.ONE_TO_MANY:
                    f.write(
                        f"""
    {field} = relationship('{type_of_field.capitalize()}Model', back_populates='{entity_name}')""" 
                    )
                elif attribute.relationship == Relationship.ONE_TO_ONE_CHILD:
                    f.write(
                        f"""
    {field}_id: Mapped[int] = mapped_column(ForeignKey("{field}.id"))
    {field}: Mapped["{field.capitalize()}Model"] = relationship(back_populates="{entity_name}") # type: ignore"""
                    )
                elif attribute.relationship == Relationship.ONE_TO_ONE_PARENT:
                    f.write(
                        f"""
    {field}: Mapped["{field.capitalize()}Model"] = relationship(back_populates="{entity_name}")"""
                    )
            else:
                f.write(
                    f"""
    {field}: {type_of_field} = Column({convert_to_sqlalchemy_type(type_of_field)})"""
                )

        f.write(timestamp_model)
