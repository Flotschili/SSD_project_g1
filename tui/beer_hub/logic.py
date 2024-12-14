from dataclasses import dataclass, field
from typing import Optional

from beer_hub_client.models import Login
from beer_hub.domain import Beer, Brewery, ID, Name


@dataclass(frozen=True, order=True)
class InMemoryBeerHub:
    __beers: list[Beer] = field(default_factory=list, init=False, repr=False)

    # only required for in-memory implementation
    def __get_highest_id(self) -> ID:
        if not self.__beers:
            return ID(-1)

        return max(beer.id for beer in self.__beers)

    def number_of_beers(self) -> int:
        return len(self.__beers)

    def get_beers(self) -> list[Beer]:
        self.__beers.sort(key=lambda beer: beer.id)
        return self.__beers

    def get_beer_by_id(self, id: ID) -> Optional[Beer]:
        return next((beer for beer in self.__beers if beer.id == id), None)

    def get_beer_by_name(self, name: Name) -> Optional[Beer]:
        return next(beer for beer in self.__beers if beer.name == name)

    def add_beer(self, beer: Beer) -> None:
        if beer.id == ID(-1):
            new_id = ID(int(self.__get_highest_id()) + 1)
            new_beer = Beer(new_id, beer.name, beer.description, beer.brewery, beer.beer_type, beer.alcohol_content)
            self.__beers.append(new_beer)
        else:
            self.__beers.append(beer)

    def update_beer_by_id(self, id: ID, beer: Beer) -> None:
        self.delete_beer_by_id(id)
        new_beer = Beer(id, beer.name, beer.description, beer.brewery, beer.beer_type, beer.alcohol_content)
        self.__beers.append(new_beer)

    def delete_beer_by_id(self, id: ID) -> None:
        self.__beers.remove(self.get_beer_by_id(id))

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
