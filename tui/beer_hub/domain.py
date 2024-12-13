from dataclasses import dataclass

from valid8 import validate

from validation.dataclasses import validate_dataclass
from validation.regex import pattern


class ValidationConstants:
    NAME_MIN_LENGTH = 1
    NAME_MAX_LENGTH = 100
    DESCRIPTION_MIN_LENGTH = 1
    DESCRIPTION_MAX_LENGTH = 250
    BREWERY_MIN_LENGTH = 1
    BREWERY_MAX_LENGTH = 100
    BEER_TYPE_MIN_LENGTH = 1
    BEER_TYPE_MAX_LENGTH = 30
    ALCOHOL_CONTENT_MIN = 0.0
    ALCOHOL_CONTENT_MAX = 75.0
    ALPHANUMERIC_SPACE_PATTERN = r'[0-9A-Za-zäöü\- ]*'

    VALID_BEER_TYPES = [
        # Pale Lagers and Pilsners
        "Pale Lager",
        "Pilsner",
        "Helles",
        "Kellerbier",
        "Zwickelbier",
        "Exportbier",

        # Amber and Dark Lagers
        "Vienna Lager",
        "Amber Lager",
        "Märzen",
        "Dunkel",
        "Schwarzbier",
        "Bock",
        "Doppelbock",
        "Eisbock",

        # Wheat Beers
        "Wheat Beer",
        "Weißbier",
        "Hefeweizen",
        "Kristallweizen",
        "Weizenbock",

        # Ales
        "Ale",
        "Pale Ale",

        # Specialty and Hybrid Styles
        "Sour",
        "Fruit Beer",

        # Non-Alcoholic and Low-Alcohol Beers
        "Non-Alcoholic Beer",
        "Low-Alcohol Beer",
        "Alcohol-Free Wheat Beer",
        "Alcohol-Free Lager",
    ]

    def __init__(self):
        raise RuntimeError(f'{self.__class__.__name__} should not be instantiated')


@dataclass(frozen=True, order=True)
class Name:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value,
                 min_len=ValidationConstants.NAME_MIN_LENGTH,
                 max_len=ValidationConstants.NAME_MAX_LENGTH,
                 custom=pattern(ValidationConstants.ALPHANUMERIC_SPACE_PATTERN))

    def __str__(self):
        return self.value


@dataclass(frozen=True, order=True)
class Description:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value,
                 min_len=ValidationConstants.DESCRIPTION_MIN_LENGTH,
                 max_len=ValidationConstants.DESCRIPTION_MAX_LENGTH,
                 custom=pattern(ValidationConstants.ALPHANUMERIC_SPACE_PATTERN))

    def __str__(self):
        return self.value

    def __len__(self):
        return len(self.value)

@dataclass(frozen=True, order=True)
class Brewery:
    value: str

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value,
                 min_len=ValidationConstants.BREWERY_MIN_LENGTH,
                 max_len=ValidationConstants.BREWERY_MAX_LENGTH,
                 custom=pattern(ValidationConstants.ALPHANUMERIC_SPACE_PATTERN))

    def __str__(self):
        return self.value


@dataclass(frozen=True, order=True)
class BeerType:
    value: str

    def __post_init__(self):
        validate_dataclass(self)

        validate('value', self.value,
                 min_len=ValidationConstants.BEER_TYPE_MIN_LENGTH,
                 max_len=ValidationConstants.BEER_TYPE_MAX_LENGTH,
                 custom=pattern(ValidationConstants.ALPHANUMERIC_SPACE_PATTERN))

        if self.value not in ValidationConstants.VALID_BEER_TYPES:
            raise ValueError(f"Invalid beer type: {self.value}")

    def __str__(self):
        return self.value


@dataclass(frozen=True, order=True)
class AlcoholContent:
    value: float

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value,
                 min_value=ValidationConstants.ALCOHOL_CONTENT_MIN,
                 max_value=ValidationConstants.ALCOHOL_CONTENT_MAX)

    @staticmethod
    def of(alcohol_content: str) -> 'AlcoholContent':
        return AlcoholContent(float(alcohol_content))

    def __str__(self):
        return f'{self.value}%'


@dataclass(frozen=True, order=True)
class ID:
    value: int

    def __post_init__(self):
        validate_dataclass(self)
        validate('value', self.value, min_value=0)

    def __str__(self):
        return str(self.value)

    def __int__(self):
        return self.value

@dataclass(frozen=True, order=True)
class Beer:
    id: ID
    name: Name
    description: Description
    brewery: Brewery
    beer_type: BeerType
    alcohol_content: AlcoholContent

    @staticmethod
    def of(name: str, description: str, brewery: str, beer_type: str, alcohol_content: float) -> 'Beer':
        return Beer(
            ID(-1),  # TODO: discuss strategy for IDs
            Name(name),
            Description(description),
            Brewery(brewery),
            BeerType(beer_type),
            AlcoholContent(alcohol_content)
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Beer):
            return NotImplemented
        return (self.name == other.name and
                self.description == other.description and
                self.brewery == other.brewery and
                self.beer_type == other.beer_type and
                self.alcohol_content == other.alcohol_content)
