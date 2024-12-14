import json

import pytest
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.test import APIClient


@pytest.fixture
def beers(db):
    return [
        mixer.blend('beers.Beer'),
        mixer.blend('beers.Beer'),
        mixer.blend('beers.Beer'),
    ]


def get_client(user=None):
    res = APIClient()
    if user is not None:
        res.force_login(user)
    return res


def parse(response):
    response.render()
    content = response.content.decode('utf-8')
    return json.loads(content)


def contains(response, key, value):
    obj = parse(response)
    if key not in obj:
        return False
    return value in obj[key]


def test_beer_anon_user_get_nothing():
    path = reverse('beers-list')
    client = get_client()
    response = client.get(path)
    assert response.status_code == HTTP_403_FORBIDDEN
    assert contains(response, 'detail', 'credentials were not provided')


def test_beer_user_get_list(beers):
    path = reverse('beers-list')
    user = mixer.blend(get_user_model())
    client = get_client(user)
    response = client.get(path)
    assert response.status_code == 200
    obj = parse(response)
    assert len(obj) == 3
