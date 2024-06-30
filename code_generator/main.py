import os
from typing import List

from base_request import Entity


def generate_main(entities: List[Entity]) -> None:
    filename = "src/main.py"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    open("src/__init__.py", "a").close()

    with open(filename, "w+") as f:
        f.write(
            f"""# -*- coding: utf-8 -*-
from fastapi import FastAPI

from src.infra.models import Base, engine
"""
        )
        models_plural = list(map(lambda model: f"{model.plural_name}", entities))
        models_plural_routers = list(
            map(lambda model: f"router_{model.plural_name}", entities)
        )
        f.write(
            f'from src.infra.api.routers import {", ".join(models_plural_routers)}\n'
        )

        f.write(
            """
Base.metadata.create_all(bind=engine)

app = FastAPI()
"""
        )

        for model in models_plural:
            f.write(f"app.include_router(router_{model})\n")
