from dataclasses import dataclass, field
from typing import Optional

from beer_hub_client.models import Login
from beer_hub.domain import Beer, Brewery


@dataclass(frozen=True, order=True)
class InMemoryBeerHub:
    __beers: list[Beer] = field(default_factory=list, init=False, repr=False)

    def number_of_beers(self) -> int:
        return len(self.__beers)

    def get_beers(self) -> list[Beer]:
        return self.__beers

    def get_beer_by_id(self, id: int) -> Optional[Beer]:
        return next(beer for beer in self.__beers if beer.id == id)

    def get_beer_by_name(self, name: str) -> Optional[Beer]:
        return next(beer for beer in self.__beers if beer.name == name)

    def add_beer(self, beer: Beer) -> None:
        self.__beers.append(beer)

    def update_beer_by_id(self, id: int, beer: Beer) -> None:
        pass

    def update_beer_by_name(self, name: str, beer: Beer) -> None:
        pass

    def delete_beer_by_id(self, id: int) -> None:
        self.__beers.remove(self.get_beer_by_id(id))

    def delete_beer_by_name(self, name: str) -> None:
        self.__beers.remove(next(beer for beer in self.__beers if beer.name == name))

    def number_of_breweries(self) -> int:
        return len(self.get_breweries())

    def get_breweries(self) -> list[Brewery]:
        return list(set({beer.brewery for beer in self.__beers}))

    def get_beers_by_brewery(self, brewery: Brewery) -> list[Beer]:
        return [beer for beer in self.__beers if beer.brewery == brewery]

    def get_beers_by_ascending_alcohol_content(self) -> list[Beer]:
        self.__beers.sort(key=lambda beer: beer.alcohol_content)
        return self.__beers

    def get_beers_by_descending_alcohol_content(self) -> list[Beer]:
        self.__beers.sort(key=lambda beer: beer.alcohol_content, reverse=True)
        return self.__beers

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
