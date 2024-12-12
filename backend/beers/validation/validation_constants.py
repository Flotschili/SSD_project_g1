ALLOWED_BEER_TYPES = [
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

MAX_ALCOHOL_CONTENT = 75.0
MIN_ALCOHOL_CONTENT = 0.00
MAX_NAME_LENGTH = 100
MAX_BREWERY_LENGTH = 100
MAX_DESCRIPTION_LENGTH = 1000

# Allowed punctuation in description
ALLOWED_DESCRIPTION_PUNCTUATION = r"[\.\,\:\;\'\"\-\!\?]"
