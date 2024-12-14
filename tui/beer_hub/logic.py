from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

from beer_hub_client import Client
from beer_hub_client.api.auth import auth_login_create
from beer_hub_client.api.beers import beers_create, beers_list, beers_read, beers_get_beer_by_name, \
    beers_get_beer_by_name_2
from beer_hub_client.models.login import Login

from beer_hub.domain import Beer, Brewery, ID, Name
from beer_hub.mapper import beer_to_dto, dto_list_to_beer_list, dto_to_beer


class BeerHub(metaclass=ABCMeta):
    @abstractmethod
    def number_of_beers(self) -> int:
        pass

    @abstractmethod
    def get_beers(self) -> list[Beer]:
        pass

    @abstractmethod
    def get_beer_by_id(self, id: ID) -> Optional[Beer]:
        pass

    @abstractmethod
    def get_beer_by_name(self, name: str) -> Optional[Beer]:
        pass

    @abstractmethod
    def add_beer(self, beer) -> None:
        pass

    @abstractmethod
    def update_beer_by_id(self, id: ID, beer: Beer) -> None:
        pass

    @abstractmethod
    def delete_beer_by_id(self, id: ID) -> None:
        pass

    @abstractmethod
    def number_of_breweries(self) -> int:
        pass

    @abstractmethod
    def get_breweries(self) -> list[Brewery]:
        pass

    @abstractmethod
    def get_beers_by_brewery(self, brewery: Brewery) -> list[Beer]:
        pass

    # TODO: Requestion life choices and remove following two methods
    @abstractmethod
    def get_beers_by_ascending_alcohol_content(self) -> list[Beer]:
        pass

    @abstractmethod
    def get_beers_by_descending_alcohol_content(self) -> list[Beer]:
        pass


@dataclass(frozen=True, order=True)
class InMemoryBeerHub(BeerHub):
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


class RESTBeerHub(BeerHub):
    __client = None

    def __init__(self, client: Client):
        self.__client = client

    @staticmethod
    def login(client: Client, username: str, password: str) -> Client:
        response = auth_login_create.sync(client=client, body=Login(username=username, password=password))
        headers = {
            "Authorization": f"Token {response.key}"
        }
        return client.with_headers(headers)

    def number_of_beers(self) -> int:
        return len(self.get_beers())

    def get_beers(self) -> list[Beer]:
        response = beers_list.sync(client=self.__client)
        return dto_list_to_beer_list(response)

    def get_beer_by_id(self, id: ID) -> Optional[Beer]:
        response = beers_read.sync(client=self.__client, id=id.value)
        return dto_to_beer(response)

    def get_beer_by_name(self, name: Name) -> Optional[Beer]:
        response = beers_get_beer_by_name_2.sync(client=self.__client, beer_name=name.value)
        return dto_to_beer(response[0] if len(response) > 0 else None) # First or None

    def add_beer(self, beer: Beer) -> None:
        dto = beer_to_dto(beer)
        beers_create.sync(client=self.__client, body=dto)

    def update_beer_by_id(self, id: ID, beer: Beer) -> None:
        pass

    def delete_beer_by_id(self, id: ID) -> None:
        pass

    def number_of_breweries(self) -> int:
        pass

    def get_breweries(self) -> list[Brewery]:
        pass

    def get_beers_by_brewery(self, brewery: Brewery) -> list[Beer]:
        pass

    def get_beers_by_ascending_alcohol_content(self) -> list[Beer]:
        pass

    def get_beers_by_descending_alcohol_content(self) -> list[Beer]:
        pass

if __name__ == '__main__':
    client = Client(base_url="http://localhost:8000/api/v1", raise_on_unexpected_status=True)

    authenticated_client = RESTBeerHub.login(client, "admin", "admin")

    bh = RESTBeerHub(authenticated_client)

    # beer = Beer(0, "Birra", "Märzen", "Halo", "Märzen", 1.0)
    #
    # bh.add_beer(beer)
    print(bh.get_beers())
    print(bh.get_beer_by_id(ID(1)))
