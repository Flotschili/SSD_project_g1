from django.core.exceptions import ValidationError
from django.db import models
from .validation.validators import (
    validate_title,
    validate_brewery,
    validate_description,
    validate_alcohol_content,
    validate_beer_type
)


class Beer(models.Model):
    name = models.CharField(
        max_length=100,
        validators=[validate_title],
        help_text="The name of the beer (capitalized)"
    )
    brewery = models.CharField(
        max_length=100,
        validators=[validate_brewery],
        help_text="Name of the brewery"
    )
    description = models.TextField(
        validators=[validate_description],
        help_text="A description of the beer"
    )
    alcohol_content = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[validate_alcohol_content],
        help_text="Alcohol by volume percentage (0.00 to 75.00)."
    )
    beer_type = models.CharField(
        max_length=100,
        validators=[validate_beer_type],
        help_text="Type of the beer"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def clean(self):
        super().clean()

        if self.beer_type == "Non-Alcoholic" and self.alcohol_content > 0.5:
            raise ValidationError({
                'alcohol_content': "Non-Alcoholic beer must not have more than 0.5% alcohol content."
            })

        if self.beer_type.startswith("Alcohol-Free") and self.alcohol_content > 0.0:
            raise ValidationError({
                'alcohol_content': "Alcohol-Free beers must have 0.0% alcohol content."
            })


    def __str__(self):
        return self.name
