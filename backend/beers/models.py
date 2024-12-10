from django.contrib.auth import get_user_model
from django.core.validators import RegexValidator
from django.db import models

from .validators import validate_title

class Beer(models.Model):
    name = models.CharField(max_length=100, validators=[validate_title])
    description = models.TextField(validators=[RegexValidator(r'^[\w\s.:;\'"]*$')])
    brewery = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name