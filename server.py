import uvicorn
from fastapi import FastAPI

from code_generator.domain.entities import generate_entity
from code_generator.seedwork.domain import generate_domain_seedwork
from code_generator.seedwork.application import generate_use_cases
from code_generator.domain.repositories import generate_repository
from code_generator.infra.models import generate_model
from code_generator.infra.repositories import generate_repository
from code_generator.application import generate_routers
from code_generator.main import generate_main
from base_request import Entity


def build_api_service(entity: Entity):
    generate_domain_seedwork()
    generate_use_cases()
    generate_entity(entity.name, entity.items)
    generate_repository(entity.name, entity.items)
    generate_model(entity.name, entity.items)
    generate_routers(entity.name, entity.items)
    generate_main([entity.name])


app = FastAPI()


@app.post("/")
async def build_api(entity: Entity):
    build_api_service(entity)
    return {"message": "api built"}


if __name__ == "__main__":
    uvicorn.run("server:app", host="0.0.0.0", port=8000, log_level="info", reload=True)