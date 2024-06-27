import os

from base_request import EntityItem, builtins_types, Relationship


def generate_dtos(entity_name: str, items: list[EntityItem]) -> None:
    filename = f"src/{entity_name}/application/dtos.py"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    open(f"src/{entity_name}/application/__init__.py", "a").close()

    with open(filename, "w+") as f:
        f.write(
            """# -*- coding: utf-8 -*-
from pydantic import BaseModel
"""
        )

        for attribute in items:
            type_of_field = attribute.type

            if type_of_field in builtins_types:
                continue

            if type_of_field == "datetime":
                f.write(f"from datetime import datetime\n")
                continue


            if attribute.relationship != Relationship.ONE_TO_ONE_CHILD:
                f.write(
                    f"from src.{type_of_field.lower()}.application.dtos import {type_of_field}\n"
                )

        f.write(
            f"""\n
class {entity_name.capitalize()}(BaseModel):
    id: int"""
        )

        for attribute in items:
            field = attribute.name
            type_of_field = attribute.type
            if field == "id":
                continue

            if attribute.relationship == Relationship.ONE_TO_ONE_CHILD:
                f.write(
                f"""
    {field}: '{type_of_field}' # type: ignore"""
            )
            else:
                f.write(
                f"""
    {field}: {type_of_field}"""
            )

        # Create Model Input
        f.write(
            f"""\n\n
class Create{entity_name.capitalize()}Input(BaseModel):
    id: int"""
        )

        for attribute in items:
            field = attribute.name
            type_of_field = attribute.type

            if field == "id":
                continue
            
            if attribute.relationship == Relationship.ONE_TO_ONE_CHILD:
                f.write(
                f"""
    {field}: '{type_of_field}' # type: ignore"""
            )
            else:
                f.write(
                f"""
    {field}: {type_of_field}"""
            )

        # Update Model Input
        f.write(
            f"""\n\n
class Update{entity_name.capitalize()}Input(BaseModel):"""
        )

        for attribute in items:
            field = attribute.name
            type_of_field = attribute.type

            if field == "id":
                continue

            if attribute.relationship == Relationship.ONE_TO_ONE_CHILD:
                f.write(
                f"""
    {field}: '{type_of_field}' # type: ignore"""
            )
            else:
                f.write(
                f"""
    {field}: {type_of_field}"""
            )
        f.write("\n")
