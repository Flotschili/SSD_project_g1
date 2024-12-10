import re
from dataclasses import dataclass, InitVar, field
from typing import Any

from valid8 import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern


@dataclass(frozen=True, order=True)
class Name:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=100, custom=pattern(r'[0-9A-Za-z ]*'))

    def __str__(self):
        return self.value


@dataclass(frozen=True, order=True)
class Brewery:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=100, custom=pattern(r'[0-9A-Za-z ]*'))

    def __str__(self):
        return self.value


@dataclass(frozen=True, order=True)
class BeerType:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_len=1, max_len=100, custom=pattern(r'[0-9A-Za-z ]*'))

    def __str__(self):
        return self.value


@dataclass(frozen=True, order=True)
class AlcoholContent:
    value: float

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_value=0.0, max_value=100.0)

    def __str__(self):
        return f'{self.value}%'


@dataclass(frozen=True, order=True)
class Beer:
    name: Name
    brewery: Brewery
    beer_type: BeerType
    alcohol_content: AlcoholContent

    @staticmethod
    def of(name: str, brewery: str, beer_type: str, alcohol_content: float) -> 'Beer':
        return Beer(
            Name(name),
            Brewery(brewery),
            BeerType(beer_type),
            AlcoholContent(alcohol_content),
        )

tmp = Beer(Name('Freistädter'), Brewery('Freistadt'), BeerType('Märzen'), AlcoholContent(4.8))

print(tmp)