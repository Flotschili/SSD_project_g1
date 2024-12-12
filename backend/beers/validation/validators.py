# validators.py
import re
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

from .validation_constants import (
    ALLOWED_BEER_TYPES,
    MAX_ALCOHOL_CONTENT, MIN_ALCOHOL_CONTENT,
    MAX_NAME_LENGTH, MAX_BREWERY_LENGTH, MAX_DESCRIPTION_LENGTH,
    ALLOWED_DESCRIPTION_PUNCTUATION
)


def validate_title(value: str) -> None:
    """Validate the beer name:
    - Must not be empty.
    - Must be capitalized (first letter uppercase).
    - Must not exceed MAX_NAME_LENGTH.
    - Should not contain disallowed characters.
    """

    if len(value.strip()) == 0:
        raise ValidationError("Name must not be empty.")

    if not value[0].isupper():
        raise ValidationError("Name must start with a capital letter.")

    if len(value) > MAX_NAME_LENGTH:
        raise ValidationError(f"Name must not exceed {MAX_NAME_LENGTH} characters.")

    #only allow letters and spaces
    if not re.match(r'^[a-zA-Z\s]*$', value):
        raise ValidationError("Name must not contain special characters.")

    # Additional character checks can be added as needed.


def validate_brewery(value: str) -> None:
    """Validate the brewery:
    - Must not be empty.
    - Must start with a capital letter.
    - Length limit enforced.
    - No HTML tags.
    """
    if len(value.strip()) == 0:
        raise ValidationError("Brewery name must not be empty.")

    if not value[0].isupper():
        raise ValidationError("Brewery name must start with a capital letter.")

    if len(value) > MAX_BREWERY_LENGTH:
        raise ValidationError(f"Brewery name must not exceed {MAX_BREWERY_LENGTH} characters.")

    # only allow letters and spaces
    if not re.match(r'^[a-zA-Z\s]*$', value):
        raise ValidationError("Name must not contain special characters.")


def validate_description(value: str) -> None:
    """Validate the beer description:
    - Length limit enforced.
    - Allowed characters include word chars, spaces, and selected punctuation.
    """
    if len(value) > MAX_DESCRIPTION_LENGTH:
        raise ValidationError(f"Description must not exceed {MAX_DESCRIPTION_LENGTH} characters.")

    # Validate allowed characters: letters, digits, whitespace, and allowed punctuation
    pattern = fr'^[\w\s{ALLOWED_DESCRIPTION_PUNCTUATION}]*$'
    if not re.match(pattern, value):
        raise ValidationError("Description contains invalid characters.")


def validate_alcohol_content(value):
    """Validate the alcohol content:
    - Must not be under MIN_ALCOHOL_CONTENT.
    - Must not exceed MAX_ALCOHOL_CONTENT.
    """
    if value < MIN_ALCOHOL_CONTENT or value > MAX_ALCOHOL_CONTENT:
        raise ValidationError(
            f"Alcohol content must be between {MIN_ALCOHOL_CONTENT} and {MAX_ALCOHOL_CONTENT} % ABV."
        )


def validate_beer_type(value: str) -> None:
    """Validate that the beer type is within the allowed domain constants."""
    if value not in ALLOWED_BEER_TYPES:
        allowed = ", ".join(ALLOWED_BEER_TYPES)
        raise ValidationError(f"Beer type must be one of the following: {allowed}.")
