import pytest
import math
from valid8 import ValidationError

from beer_hub.domain import (
    Name, Description, Brewery, BeerType, AlcoholContent, ID, Beer,
    ValidationConstants
)


def test_validation_constants_cannot_be_instantiated():
    with pytest.raises(RuntimeError):
        ValidationConstants()


def test_name_valid_creation():
    name = Name("Test Beer")
    assert str(name) == "Test Beer"
    assert name.value == "Test Beer"


def test_name_validation_errors():
    with pytest.raises(ValidationError):
        Name("")  # too short
    with pytest.raises(ValidationError):
        Name("a" * 101)  # too long
    with pytest.raises(ValidationError):
        Name("Invalid$Name")  # invalid characters


def test_name_comparison():
    assert Name("Beer A") < Name("Beer B")
    assert Name("Beer A") == Name("Beer A")
    assert Name("Beer B") > Name("Beer A")


def test_description_valid_creation():
    desc = Description("A tasty beer")
    assert str(desc) == "A tasty beer"
    assert desc.value == "A tasty beer"
    assert len(desc) == len("A tasty beer")


def test_description_validation_errors():
    with pytest.raises(ValidationError):
        Description("")  # too short
    with pytest.raises(ValidationError):
        Description("a" * 251)  # too long
    with pytest.raises(ValidationError):
        Description("Invalid$Description")  # invalid characters


def test_description_comparison():
    assert Description("Desc A") < Description("Desc B")
    assert Description("Desc A") == Description("Desc A")


def test_brewery_valid_creation():
    brewery = Brewery("Test Brewery")
    assert str(brewery) == "Test Brewery"
    assert brewery.value == "Test Brewery"


def test_brewery_validation_errors():
    with pytest.raises(ValidationError):
        Brewery("")  # too short
    with pytest.raises(ValidationError):
        Brewery("a" * 101)  # too long
    with pytest.raises(ValidationError):
        Brewery("Invalid$Brewery")  # invalid characters


def test_beer_type_valid_creation():
    beer_type = BeerType("Pilsner")
    assert str(beer_type) == "Pilsner"
    assert beer_type.value == "Pilsner"


def test_beer_type_validation_errors():
    with pytest.raises(ValidationError):
        BeerType("")  # too short
    with pytest.raises(ValidationError):
        BeerType("a" * 31)  # too long
    with pytest.raises(ValidationError):
        BeerType("Invalid$Type")  # invalid characters
    with pytest.raises(ValueError):
        BeerType("Invalid Beer Type")  # not in valid types list


def test_alcohol_content_valid_creation():
    alcohol = AlcoholContent(5.0)
    assert str(alcohol) == "5.0 %"
    assert math.isclose(alcohol.value, 5.0, rel_tol=1e-09, abs_tol=1e-09)


def test_alcohol_content_of_method():
    alcohol = AlcoholContent.of("5.0 %")
    assert math.isclose(alcohol.value, 5.0, rel_tol=1e-09, abs_tol=1e-09)


def test_alcohol_content_validation_errors():
    with pytest.raises(ValidationError):
        AlcoholContent(-0.1)  # too low
    with pytest.raises(ValidationError):
        AlcoholContent(75.1)  # too high


def test_id_valid_creation():
    id_obj = ID(1)
    assert str(id_obj) == "1"
    assert int(id_obj) == 1
    assert id_obj.value == 1


def test_id_validation_errors():
    with pytest.raises(ValidationError):
        ID(-2)  # less than -1


def test_beer_creation():
    beer = Beer(
        ID(1),
        Name("Test Beer"),
        Description("A test beer"),
        Brewery("Test Brewery"),
        BeerType("Pilsner"),
        AlcoholContent(5.0)
    )
    assert beer.id.value == 1
    assert beer.name.value == "Test Beer"


def test_beer_of_factory_method():
    beer = Beer.of(
        Name("Test Beer"),
        Description("A test beer"),
        Brewery("Test Brewery"),
        BeerType("Pilsner"),
        AlcoholContent(5.0)
    )
    assert beer.id.value == -1  # default ID for new beers


def test_beer_parse_method():
    beer = Beer.parse(
        1,
        "Test Beer",
        "A test beer",
        "Test Brewery",
        "Pilsner",
        "5.0 %"
    )
    assert beer.id.value == 1
    assert beer.name.value == "Test Beer"
    assert math.isclose(beer.alcohol_content.value, 5.0, rel_tol=1e-09, abs_tol=1e-09)


def test_beer_equality():
    beer1 = Beer.parse(1, "Test Beer", "A test beer", "Test Brewery", "Pilsner", "5.0 %")
    beer2 = Beer.parse(2, "Test Beer", "A test beer", "Test Brewery", "Pilsner", "5.0 %")
    beer3 = Beer.parse(3, "Different Beer", "A test beer", "Test Brewery", "Pilsner", "5.0 %")

    assert beer1 == beer2  # IDs are ignored in equality
    assert beer1 != beer3
    assert beer1 != "not a beer"  # test comparison with different type


def test_beer_ordering():
    beer1 = Beer.parse(1, "Beer A", "A test beer", "Test Brewery", "Pilsner", "5.0 %")
    beer2 = Beer.parse(2, "Beer B", "A test beer", "Test Brewery", "Pilsner", "5.0 %")

    assert beer1 < beer2
