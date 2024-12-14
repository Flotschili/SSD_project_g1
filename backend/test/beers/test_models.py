import pytest
from django.core.exceptions import ValidationError
from mixer.backend.django import mixer

from beers.validation.validation_constants import MAX_NAME_LENGTH, MAX_DESCRIPTION_LENGTH, MAX_BREWERY_LENGTH

@pytest.fixture
def beer_args():
    return {
        'name': 'Valid Beer Name',
        'brewery': 'Valid Brewery',
        'description': 'A valid description.',
        'alcohol_content': '5.0',
        'beer_type': 'Pale Lager'
    }


@pytest.mark.django_db
class TestBeerNameValidation:
    def test_name_too_long_raises_validation_error(self, beer_args):
        beer_args['name'] = 'A' * (MAX_NAME_LENGTH + 1)
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()

    def test_name_empty_raises_validation_error(self, beer_args):
        beer_args['name'] = ''
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()

    def test_name_with_invalid_characters_raises_validation_error(self, beer_args):
        beer_args['name'] = 'Invalid@Name!'
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()

    def test_name_not_capitalized_raises_validation_error(self, beer_args):
        beer_args['name'] = 'lowercase name'
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()

    def test_name_all_spaces_or_whitespace_raises_validation_error(self, beer_args):
        beer_args['name'] = '   '
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()

    def test_name_valid_passes_validation(self, beer_args):
        beer_args['name'] = 'Valid Beer Name'
        beer_args['brewery'] = 'Valid Brewery'
        beer_args['description'] = 'A valid description.'
        beer_args['alcohol_content'] = '5.0'
        beer_args['beer_type'] = 'Pale Lager'

        beer = mixer.blend('beers.Beer', **beer_args)
        beer.full_clean()


@pytest.mark.django_db
class TestBeerBreweryValidation:
    def test_brewery_too_long_raises_validation_error(self, beer_args):
        beer_args['brewery'] = 'A' * (MAX_BREWERY_LENGTH + 1)
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()

    def test_brewery_empty_raises_validation_error(self, beer_args):
        beer_args['brewery'] = ''
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()

    def test_brewery_not_capitalized_raises_validation_error(self, beer_args):
        beer_args['brewery'] = 'lowercase brewery'
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()

    def test_brewery_with_invalid_characters_raises_validation_error(self, beer_args):
        beer_args['brewery'] = 'Invalid@Brewery!'
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()

    def test_brewery_valid_passes_validation(self, beer_args):
        beer_args['brewery'] = 'Valid Brewery Name'
        beer_args['name'] = 'Valid Name'
        beer_args['description'] = 'A valid description.'
        beer_args['alcohol_content'] = '5.0'
        beer_args['beer_type'] = 'Pale Lager'

        beer = mixer.blend('beers.Beer', **beer_args)
        beer.full_clean()


@pytest.mark.django_db
class TestBeerDescriptionValidation:
    def test_description_too_long_raises_validation_error(self, beer_args):
        beer_args['description'] = 'A' * (MAX_DESCRIPTION_LENGTH + 1)
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()
        assert 'Description must not exceed' in str(err.value)

    def test_description_with_invalid_characters_raises_validation_error(self, beer_args):
        beer_args['description'] = 'Invalid description with #$%'
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()
        assert 'Description contains invalid characters' in str(err.value)

    def test_description_valid_passes_validation(self, beer_args):
        beer_args['description'] = (
            "A well-crafted beer. Notes of citrus, tropical fruit, and caramel."
        )
        beer_args['name'] = 'Valid Name'
        beer_args['brewery'] = 'Valid Brewery'
        beer_args['alcohol_content'] = '5.0'
        beer_args['beer_type'] = 'Pale Lager'

        beer = mixer.blend('beers.Beer', **beer_args)
        beer.full_clean()

    def test_description_with_allowed_punctuation_passes_validation(self, beer_args):
        beer_args['description'] = (
            "This beer has a robust flavor: hoppy, malty, and well-balanced!"
        )
        beer_args['name'] = 'Valid Name'
        beer_args['brewery'] = 'Valid Brewery'
        beer_args['alcohol_content'] = '5.0'
        beer_args['beer_type'] = 'Pale Lager'

        beer = mixer.blend('beers.Beer', **beer_args)
        beer.full_clean()

@pytest.mark.django_db
class TestBeerAlcoholContentValidation:
    def test_alcohol_content_negative_raises_validation_error(self, beer_args):
        beer_args['alcohol_content'] = '-1.0'
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()

    def test_alcohol_content_excessive_raises_validation_error(self, beer_args):
        beer_args['alcohol_content'] = '100.1'
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()

    def test_alcohol_content_valid_passes_validation(self, beer_args):
        beer_args['alcohol_content'] = '5.0'
        beer = mixer.blend('beers.Beer', **beer_args)
        beer.full_clean()

@pytest.mark.django_db
class TestBeerTypeValidation:
    def test_beer_type_empty_raises_validation_error(self, beer_args):
        beer_args['beer_type'] = ''
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()

    def test_beer_type_invalid_choice_raises_validation_error(self, beer_args):
        beer_args['beer_type'] = 'InvalidType'
        beer = mixer.blend('beers.Beer', **beer_args)
        with pytest.raises(ValidationError) as err:
            beer.full_clean()

    def test_beer_type_valid_passes_validation(self, beer_args):
        beer_args['beer_type'] = 'Pale Lager'
        beer = mixer.blend('beers.Beer', **beer_args)
        beer.full_clean()
