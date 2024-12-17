from beer_hub_client.types import Unset

from beer_hub import domain
from beer_hub_client import models
from typing import Optional


def beer_to_dto(beer: domain.Beer) -> Optional[models.beer.Beer]:
    """Convert domain Beer to DTO Beer"""
    if beer is None:
        return None

    return models.beer.Beer(
        name=beer.name.value,
        description=beer.description.value,
        brewery=beer.brewery.value,
        beer_type=beer.beer_type.value,
        alcohol_content=str(beer.alcohol_content.value)
    )


def dto_to_beer(dto: models.beer.Beer | None) -> Optional[domain.Beer]:
    """Convert DTO Beer to domain Beer"""
    if dto is None:
        return None

    id_value = dto.id if not isinstance(dto.id, Unset) else -1

    return domain.Beer.parse(
        id=int(id_value),
        name=dto.name,
        description=dto.description,
        brewery=dto.brewery,
        beer_type=dto.beer_type,
        alcohol_content=dto.alcohol_content
    )


def dto_list_to_beer_list(dto: list[models.beer.Beer]) -> list[domain.Beer]:
    """Convert list of DTO Beers to list of domain Beers"""
    return [dto_to_beer(beer_dto) for beer_dto in dto]
