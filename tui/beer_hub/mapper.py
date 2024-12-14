from beer_hub import domain
from beer_hub_client.models.beer import Beer

def beer_to_dto(beer: domain.Beer):
    return Beer(
        name=beer.name,
        description=beer.description,
        brewery=beer.brewery
    )