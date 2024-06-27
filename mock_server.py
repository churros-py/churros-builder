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
from base_request import Entity, EntityItem, convert_entity_type, Relationship


def build_api_service(entities: list[Entity]):
    generate_domain_seedwork()
    generate_use_cases()

    for entity in entities:
        for item in entity.items:
            item.type = convert_entity_type(item.type)

        filtered_items = [item for item in entity.items if item.relationship != Relationship.ONE_TO_MANY]

        generate_entity(entity.name, filtered_items)
        generate_domain_repository(entity.name)
        generate_repository(entity.name, filtered_items)
        generate_model(entity.name, entity.items)
        generate_routers(entity.name, filtered_items)

    generate_main([entity.name for entity in entities])

user_items = [
    EntityItem(name="name", type="str"),
    EntityItem(name="products", type="product", relationship=Relationship.ONE_TO_MANY),
    EntityItem(name="address", type="address", relationship=Relationship.ONE_TO_ONE_PARENT),
]

product_items = [
    EntityItem(name="name", type="str"),
    EntityItem(name="expiration_date", type="datetime"),
    EntityItem(name="quantity", type="int", has_default_value=True, default_value=10),
    EntityItem(name="weight", type="float", has_default_value=True, default_value=0.0),
    EntityItem(
        name="description",
        type="str",
        has_default_value=True,
        default_value="no description",
    ),
    EntityItem(name="active", type="bool", has_default_value=True, default_value=False),
    EntityItem(name="user", type="user", relationship=Relationship.MANY_TO_ONE),
]

address_items = [
    EntityItem(name="street", type="str", has_default_value=False),
    EntityItem(name="user", type="user", relationship=Relationship.ONE_TO_ONE_CHILD),
]

address = Entity(name='address', items=address_items)
user = Entity(name="user", items=user_items)
product = Entity(name="product", items=product_items)

build_api_service([product, user, address])
