from dataclasses import dataclass, field

from beer_hub_client.models import Login
from valid8 import validate

from beer_hub.domain import Beer, Brewery


@dataclass(frozen=True, order=True)
class BeerHub:
    __beers: list[Beer] = field(default_factory=list, init=False, repr=False)

    def number_of_beers(self) -> int:
        return len(self.__beers)

    def beer_at_index(self, index) -> Beer:
        validate('index', index, min_value=0, max_value=len(self.__beers) - 1)
        return self.__beers[index]

    def add_beer(self, beer: Beer) -> None:
        self.__beers.append(beer)

    def remove_beer(self, index: int) -> None:
        self.__beers.pop(index)

    def list_of_breweries(self) -> list[Brewery]:
        return list({beer.brewery for beer in self.__beers})

    def beers_of_brewery(self, brewery: Brewery) -> list[Beer]:
        return [beer for beer in self.__beers if beer.brewery == brewery]

    def sort_by_ascending_alcohol_content(self) -> None:
        self.__beers.sort(key=lambda beer: beer.alcohol_content)

    def __iter__(self):
        return iter(self.__beers)

    def __len__(self):
        return len(self.__beers)


def ping_backend():
    from beer_hub_client import Client
    from beer_hub_client.api.auth import auth_login_create

    client = Client(base_url="http://127.0.0.1:8000")

    response = auth_login_create.sync(client=client, body=Login("admin", "admin"))
    print(response)
