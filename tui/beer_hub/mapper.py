from beer_hub import domain
from beer_hub_client import models
from typing import Optional


def beer_to_dto(beer: domain.Beer) -> Optional[models.beer.Beer]:
    if beer is None:
        return None

    return models.beer.Beer(
        name=beer.name.value,
        description=beer.description.value,
        brewery=beer.brewery.value,
        beer_type=beer.beer_type.value,
        alcohol_content=beer.alcohol_content.value
    )


def dto_to_beer(dto: models.beer.Beer) -> Optional[domain.Beer]:
    if dto is None:
        return None

    return domain.Beer.parse(
        id=dto.id,
        name=dto.name,
        description=dto.description,
        brewery=dto.brewery,
        beer_type=dto.beer_type,
        alcohol_content=dto.alcohol_content
    )


def dto_list_to_beer_list(dto: list[models.beer.Beer]) -> list[domain.Beer]:
    return [dto_to_beer(beer_dto) for beer_dto in dto]
