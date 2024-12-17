import math

import pytest
from typeguard import TypeCheckError

from beer_hub import domain
from beer_hub_client import models, types

from beer_hub.domain import ID
from beer_hub.mapper import beer_to_dto, dto_to_beer, dto_list_to_beer_list


@pytest.fixture
def sample_domain_beer():
    """Fixture providing a sample domain Beer object"""
    return domain.Beer.parse(
        id=1,
        name="Test Beer",
        description="A test beer description",
        brewery="Test Brewery",
        beer_type="Pilsner",
        alcohol_content="5.0 %"
    )


@pytest.fixture
def sample_dto_beer():
    """Fixture providing a sample DTO Beer object"""
    return models.beer.Beer(
        id=1,
        name="Test Beer",
        description="A test beer description",
        brewery="Test Brewery",
        beer_type="Pilsner",
        alcohol_content="5.0"
    )


class TestBeerToDto:
    """Tests for beer_to_dto conversion function"""

    def test_none_raises_type_error(self):
        """Test that None input raises TypeCheckError"""
        with pytest.raises(TypeCheckError):
            beer_to_dto(None)

    def test_valid_conversion(self, sample_domain_beer):
        """Test conversion of valid domain beer to DTO"""
        dto = beer_to_dto(sample_domain_beer)
        assert dto is not None
        assert dto.name == sample_domain_beer.name.value
        assert dto.description == sample_domain_beer.description.value
        assert dto.brewery == sample_domain_beer.brewery.value
        assert dto.beer_type == sample_domain_beer.beer_type.value
        assert math.isclose(float(dto.alcohol_content),
                            sample_domain_beer.alcohol_content.value,
                            rel_tol=1e-09, abs_tol=1e-09)

    def test_special_characters(self):
        """Test handling of special characters in conversion"""
        beer = domain.Beer.parse(
            id=1,
            name="Bier mit Umlauts äöü",
            description="Special chars: - .",
            brewery="Brauerei",
            beer_type="Pilsner",
            alcohol_content="5.0 %"
        )
        dto = beer_to_dto(beer)
        assert dto.name == "Bier mit Umlauts äöü"
        assert dto.description == "Special chars: - ."
        assert dto.brewery == "Brauerei"


class TestDtoToBeer:
    """Tests for dto_to_beer conversion function"""
    def test_none_returns_none(self):
        """Test that None input returns None"""
        assert dto_to_beer(None) is None

    def test_valid_conversion(self, sample_dto_beer):
        """Test conversion of valid DTO to domain beer"""
        beer = dto_to_beer(sample_dto_beer)
        assert beer is not None
        assert beer.name.value == sample_dto_beer.name
        assert beer.description.value == sample_dto_beer.description
        assert beer.brewery.value == sample_dto_beer.brewery
        assert beer.beer_type.value == sample_dto_beer.beer_type

        assert math.isclose(beer.alcohol_content.value,
                            float(sample_dto_beer.alcohol_content),
                            rel_tol=1e-09, abs_tol=1e-09)

    def test_unset_id(self):
        """Test handling of Unset ID"""
        dto = models.beer.Beer(
            id=types.Unset(),
            name="Test Beer",
            description="Description",
            brewery="Brewery",
            beer_type="Pilsner",
            alcohol_content="5.0"
        )
        beer = dto_to_beer(dto)
        assert beer is not None
        assert beer.id == ID(-1)


class TestDtoListToBeerList:
    """Tests for dto_list_to_beer_list conversion function"""

    def test_empty_list(self):
        """Test conversion of empty list"""
        assert dto_list_to_beer_list([]) == []

    def test_single_item(self, sample_dto_beer):
        """Test conversion of single-item list"""
        beer_list = dto_list_to_beer_list([sample_dto_beer])
        assert len(beer_list) == 1
        assert isinstance(beer_list[0], domain.Beer)
        assert beer_list[0].name.value == sample_dto_beer.name

    def test_multiple_items(self):
        """Test conversion of multiple items with varying values"""
        dtos = [
            models.beer.Beer(
                id=1,
                name="Beer 1",
                description="Desc 1",
                brewery="Brewery 1",
                beer_type="Pilsner",
                alcohol_content="5.0"
            ),
            models.beer.Beer(
                id=types.Unset(),
                name="Beer 2",
                description="Desc 2",
                brewery="Brewery 2",
                beer_type="Helles",
                alcohol_content="6.5"
            )
        ]

        beers = dto_list_to_beer_list(dtos)
        assert len(beers) == 2
        assert beers[0].id == ID(1)
        assert beers[1].id == ID(-1)
        assert beers[0].name.value == "Beer 1"
        assert beers[1].name.value == "Beer 2"

    def test_maintains_order(self):
        """Test that list conversion maintains the order of items"""
        dtos = [
            models.beer.Beer(
                id=1,
                name="Beer A",
                description="Desc",
                brewery="Brewery",
                beer_type="Pilsner",
                alcohol_content="5.0"
            ),
            models.beer.Beer(
                id=2,
                name="Beer B",
                description="Desc",
                brewery="Brewery",
                beer_type="Pilsner",
                alcohol_content="6.0"
            )
        ]
        beers = dto_list_to_beer_list(dtos)
        assert [beer.name.value for beer in beers] == ["Beer A", "Beer B"]


def test_round_trip_conversion(sample_domain_beer):
    """Test that converting domain -> DTO -> domain preserves data"""
    dto = beer_to_dto(sample_domain_beer)
    converted_beer = dto_to_beer(dto)

    assert converted_beer.name == sample_domain_beer.name
    assert converted_beer.description == sample_domain_beer.description
    assert converted_beer.brewery == sample_domain_beer.brewery
    assert converted_beer.beer_type == sample_domain_beer.beer_type
    assert converted_beer.alcohol_content == sample_domain_beer.alcohol_content
