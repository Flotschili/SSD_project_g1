import json

import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.test import APIClient

# ToDo: Add tests here