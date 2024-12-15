import json

import pytest
from unittest.mock import MagicMock, patch

from beer_hub_client.errors import UnexpectedStatus

from beer_hub.domain import *
from beer_hub.logic import RESTBeerHub, InMemoryBeerHub
from beer_hub_client import models

from beer_hub.mapper import beer_to_dto

# Sample beers for testing
test_beers = [
    Beer(
        id=ID(1),
        name=Name("Test Beer One"),
        description=Description("A sample beer description."),
        brewery=Brewery("Sample Brewery"),
        beer_type=BeerType("Ale"),
        alcohol_content=AlcoholContent(5.0)
    ),
    Beer(
        id=ID(2),
        name=Name("Test Beer Two"),
        description=Description("Another sample beer description."),
        brewery=Brewery("Another Brewery"),
        beer_type=BeerType("Pilsner"),
        alcohol_content=AlcoholContent(4.5)
    )
]
test_dtos = [beer_to_dto(beer) for beer in test_beers]


# Fixtures
@pytest.fixture
def client_mock():
    return MagicMock()


@pytest.fixture
def rest_beer_hub(client_mock):
    return RESTBeerHub(client=client_mock)


def test_login_success(client_mock):
    with patch("beer_hub_client.api.auth.auth_login_create.sync") as login_mock:
        login_mock.return_value.key = "test_token"
        logged_in_client = RESTBeerHub.login(client_mock, "user", "pass")

        assert logged_in_client is not None
        login_mock.assert_called_once()
        client_mock.with_headers.assert_called_once_with({"Authorization": "Token test_token"})


def test_login_failure(client_mock):
    with patch("beer_hub_client.api.auth.auth_login_create.sync", side_effect=UnexpectedStatus(300, b'test_failed')):
        logged_in_client = RESTBeerHub.login(client_mock, "user", "wrong_pass")

        assert logged_in_client is None


def test_number_of_beers(rest_beer_hub):
    with patch.object(rest_beer_hub, "get_beers", return_value=[1, 2, 3]):
        assert rest_beer_hub.number_of_beers() == 3


def test_get_beers(rest_beer_hub):
    with patch("beer_hub_client.api.beers.beers_list.sync", return_value=test_dtos) as beers_list_mock:
        beers = rest_beer_hub.get_beers()

        beers_list_mock.assert_called_once_with(client=rest_beer_hub._RESTBeerHub__client)
        assert beers == test_beers


def test_get_beer_by_id(rest_beer_hub):
    with patch("beer_hub_client.api.beers.beers_read.sync", return_value=test_dtos[0]) as beers_read_mock:
        beer = rest_beer_hub.get_beer_by_id(MagicMock(value=1))

        beers_read_mock.assert_called_once_with(client=rest_beer_hub._RESTBeerHub__client, id=1)
        assert beer == test_beers[0]


def test_get_beer_by_name(rest_beer_hub):
    with patch("beer_hub_client.api.beers.beers_get_beer_by_name_2.sync", return_value=test_dtos) as get_by_name_mock:
        beer = rest_beer_hub.get_beer_by_name(MagicMock(value="Test Beer"))

        get_by_name_mock.assert_called_once_with(client=rest_beer_hub._RESTBeerHub__client, beer_name="Test Beer")
        assert beer == test_beers[0]


def test_add_beer(rest_beer_hub):
    with patch("beer_hub_client.api.beers.beers_create.sync") as beers_create_mock:
        rest_beer_hub.add_beer(test_beers[0])

        beers_create_mock.assert_called_once_with(client=rest_beer_hub._RESTBeerHub__client, body=test_dtos[0])


def test_update_beer_by_id(rest_beer_hub):
    with patch("beer_hub_client.api.beers.beers_update.sync") as beers_update_mock:
        rest_beer_hub.update_beer_by_id(MagicMock(value=1), test_beers[0])

        beers_update_mock.assert_called_once_with(client=rest_beer_hub._RESTBeerHub__client, id=1, body=test_dtos[0])


def test_delete_beer_by_id(rest_beer_hub):
    with patch("beer_hub_client.api.beers.beers_delete.sync_detailed") as beers_delete_mock:
        rest_beer_hub.delete_beer_by_id(MagicMock(value=1))

        beers_delete_mock.assert_called_once_with(client=rest_beer_hub._RESTBeerHub__client, id=1)


def test_number_of_breweries(rest_beer_hub):
    response_mock = MagicMock()
    response_mock.content.decode.return_value = '{"count": 10}'

    with patch("beer_hub_client.api.breweries.breweries_number_of_breweries.sync_detailed", return_value=response_mock):
        count = rest_beer_hub.number_of_breweries()

        assert count == 10


def test_get_breweries(rest_beer_hub):
    response_mock = MagicMock()
    response_mock.content.decode.return_value = '["BreweryOne", "BreweryTwo"]'
    with patch("beer_hub_client.api.list_breweries.list_breweries.sync_detailed", return_value=response_mock):
        breweries = rest_beer_hub.get_breweries()

        assert breweries == [Brewery("BreweryOne"), Brewery("BreweryTwo")]


def test_get_beers_by_brewery(rest_beer_hub):
    response_mock = MagicMock()
    response_mock.content.decode.return_value = '''
    [{
      "id": 1,
      "name": "Test Beer One",
      "description": "A sample beer description.",
      "brewery": "Sample Brewery",
      "beer_type": "Ale",
      "alcohol_content": "5.0"
    }]
    '''
    with patch("beer_hub_client.api.breweries.breweries_get_beers_by_brewery.sync_detailed",
               return_value=response_mock):
        beers = rest_beer_hub.get_beers_by_brewery(MagicMock(value="Sample Brewery"))

        assert len(beers) == 1
        assert beers[0] == test_beers[0]


def test_get_beers_by_ascending_alcohol_content(rest_beer_hub):
    with patch.object(rest_beer_hub, "get_beers",
                      return_value=[MagicMock(alcohol_content=5.5), MagicMock(alcohol_content=4.5)]):
        beers = rest_beer_hub.get_beers_by_ascending_alcohol_content()

        assert beers[0].alcohol_content == 4.5
        assert beers[1].alcohol_content == 5.5


def test_get_beers_by_descending_alcohol_content(rest_beer_hub):
    with patch.object(rest_beer_hub, "get_beers",
                      return_value=[MagicMock(alcohol_content=4.5), MagicMock(alcohol_content=5.5)]):
        beers = rest_beer_hub.get_beers_by_descending_alcohol_content()

        assert beers[0].alcohol_content == 5.5
        assert beers[1].alcohol_content == 4.5


# Additional tests for InMemoryBeerHub
def test_get_beer_by_name_in_memory():
    beer_hub = InMemoryBeerHub()
    [beer_hub.add_beer(beer) for beer in test_beers]

    beer = beer_hub.get_beer_by_name(test_beers[0].name)

    assert beer == test_beers[0]


def test_update_beer_by_id_in_memory():
    beer_hub = InMemoryBeerHub()
    test_beer = Beer(ID(1), Name("Beer One"), Description("description"), Brewery("Brewery"),
                        BeerType("Ale"), AlcoholContent(6.0))
    beer_hub.add_beer(test_beer)

    updated_beer = Beer(ID(1), Name("Updated Beer One"), Description("Updated description"), Brewery("Updated Brewery"),
                        BeerType("Ale"), AlcoholContent(6.0))

    beer_hub.update_beer_by_id(ID(1), updated_beer)

    assert beer_hub.get_beer_by_id(ID(1)) == updated_beer


def test_get_beers_by_ascending_alcohol_content_in_memory():
    beer_hub = InMemoryBeerHub()
    [beer_hub.add_beer(beer) for beer in test_beers]

    sorted_beers = beer_hub.get_beers_by_ascending_alcohol_content()

    assert sorted_beers[0].alcohol_content < sorted_beers[1].alcohol_content

def test_get_beers_by_descending_alcohol_content_in_memory():
    beer_hub = InMemoryBeerHub()
    [beer_hub.add_beer(beer) for beer in test_beers]

    sorted_beers = beer_hub.get_beers_by_descending_alcohol_content()

    assert sorted_beers[0].alcohol_content > sorted_beers[1].alcohol_content

def test_add_beer_with_unknown_id():
    beer_hub = InMemoryBeerHub()
    test_beer = Beer(ID(-1), Name("Beer One"), Description("description"), Brewery("Brewery"),
                     BeerType("Ale"), AlcoholContent(6.0))

    beer_hub.add_beer(test_beer)

    beer = beer_hub.get_beer_by_name(test_beer.name)

    assert beer == test_beer

def test_number_of_beers_in_memory():
    beer_hub = InMemoryBeerHub()
    [beer_hub.add_beer(beer) for beer in test_beers]

    assert beer_hub.number_of_beers() == len(test_beers)

def test_get_beers_in_memory():
    beer_hub = InMemoryBeerHub()
    [beer_hub.add_beer(beer) for beer in test_beers]

    returned_beers = beer_hub.get_beers()

    assert returned_beers == test_beers

def test_number_of_breweries_in_memory():
    beer_hub = InMemoryBeerHub()
    [beer_hub.add_beer(beer) for beer in test_beers]

    assert beer_hub.number_of_breweries() == 2

def test_get_breweries_in_memory():
    beer_hub = InMemoryBeerHub()
    [beer_hub.add_beer(beer) for beer in test_beers]

    breweries = beer_hub.get_breweries()

    assert len(breweries) == 2
    assert test_beers[0].brewery in breweries
    assert test_beers[1].brewery in breweries

def test_get_beers_by_brewery_in_memory():
    beer_hub = InMemoryBeerHub()
    [beer_hub.add_beer(beer) for beer in test_beers]

    beers_by_brewery = beer_hub.get_beers_by_brewery(test_beers[0].brewery)

    assert len(beers_by_brewery) == 1
    assert beers_by_brewery[0] == test_beers[0]
