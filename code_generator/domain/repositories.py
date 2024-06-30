import os


def generate_repository(entity_name: str, plural_entity_name: str) -> None:
    filename = f"src/{entity_name}/domain/repositories.py"
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    model_lower = entity_name
    model = entity_name.capitalize()

    with open(filename, "w+") as f:
        f.write(
            f"""
# -*- coding: utf-8 -*-
from typing import Tuple
from abc import ABCMeta, abstractmethod

from src.{model_lower}.domain.entities import {model}


class {model}Repository(metaclass=ABCMeta):
    @abstractmethod
    def find_all(self) -> Tuple[{model}]:
        \"""
        Method responsable for find all {plural_entity_name} considering pagination
        \"""
        pass

    @abstractmethod
    def find_by_id(self, {model_lower}_id: int) -> {model} | None:
        \"""
        Method responsable for find {model_lower} by id
        \"""
        pass

    @abstractmethod
    def save(self, input_save_{model_lower}) -> {model}:
        \"""
        Method responsable for save {model_lower}
        \"""
        pass

    @abstractmethod
    def update(self, input_update_{model_lower}) -> {model}:
        \"""
        Method responsable for update {model_lower}
        \"""
        pass

    @abstractmethod
    def inactivate(self, {model_lower}_id: int) -> None:
        \"""
        Method responsable for inactive {model_lower}
        \"""
        pass

    @abstractmethod
    def delete(self, {model_lower}_id: int) -> None:
        \"""
        Method responsable for delete {model_lower}
        \"""
        pass
"""
        )
