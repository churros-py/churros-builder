from pydantic import BaseModel
from typing import Optional, Any

from code_generator.common.type_helper import CustomEnum


builtins_types = ["str", "int", "float", "bool"]


def convert_entity_type(name: str) -> str:
    if name in builtins_types:
        return name
    if name == "datetime":
        return name

    return name.capitalize()


class Relationship(CustomEnum):
    ONE_TO_ONE_PARENT = "OneToOneParent"
    ONE_TO_ONE_CHILD = "OneToOneChild"
    ONE_TO_MANY = "OneToMany"
    MANY_TO_ONE = "ManyToOne" # I Know, doesn't make sense. But I can explain
    MANY_TO_MANY = "ManyToMany"


class EntityItem(BaseModel):
    name: str
    type: str
    default_value: Optional[Any]
    has_default_value: Optional[bool] = False
    relationship: Optional[Relationship] = None


class Entity(BaseModel):
    name: str
    items: list[EntityItem]
