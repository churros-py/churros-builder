import uvicorn
from fastapi import FastAPI

from code_generator.domain.entities import generate_entity
from code_generator.seedwork.domain import generate_domain_seedwork
from code_generator.seedwork.application import generate_use_cases
from code_generator.domain.repositories import (
    generate_repository as generate_domain_repository,
)
from code_generator.infra.models import generate_model
from code_generator.infra.repositories import generate_repository
from code_generator.application import generate_routers
from code_generator.main import generate_main
from base_request import Entity, convert_entity_type


def build_api_service(entities: list[Entity]):
    generate_domain_seedwork()
    generate_use_cases()

    for entity in entities:
        for item in entity.items:
            item.type = convert_entity_type(item.type)

        generate_entity(entity.name, entity.items)
        generate_domain_repository(entity.name, entity.plural_name)
        generate_repository(entity.name, entity.plural_name, entity.items)
        generate_model(entity.name, entity.plural_name, entity.items)
        generate_routers(entity.name, entity.plural_name, entity.items)

    generate_main([entity.name for entity in entities])


app = FastAPI()


@app.post("/")
async def build_api(entities: list[Entity]):
    build_api_service(entities)
    return {"message": "api built"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8001, log_level="info", reload=True)
