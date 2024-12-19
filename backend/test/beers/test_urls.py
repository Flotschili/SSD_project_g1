import pytest
import json
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse
from rest_framework.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_204_NO_CONTENT, HTTP_403_FORBIDDEN, \
    HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND
from mixer.backend.django import mixer
from rest_framework.test import APIClient

def get_client(user=None):
    client = APIClient()
    if user is not None:
        client.force_login(user)
    return client

# Fixtures
@pytest.fixture
def standard_user(db):
    user = get_user_model()
    return user.objects.create_user(username="testuser", password="testpass")

@pytest.fixture
def client_with_user(standard_user):
    return get_client(user=standard_user)

@pytest.fixture
def admin_user(db):
    user = get_user_model()
    group = mixer.blend('auth.Group', name='beer_editor')
    admin = user.objects.create_user(username="admin", password="adminpass", is_staff=True, is_superuser=True)
    admin.groups.add(group)
    admin.save()
    return admin

@pytest.fixture
def client_with_admin(admin_user):
    return get_client(user=admin_user)

@pytest.fixture
def beer(db):
    return mixer.blend("beers.Beer", name="Test Beer", brewery="Test Brewery")

@pytest.fixture
def beers(db):
    return [
        mixer.blend("beers.Beer", name="Beer 1", brewery="Brewery 1"),
        mixer.blend("beers.Beer", name="Beer 2", brewery="Brewery 2"),
    ]

@pytest.fixture
def valid_beer_args():
    return {
        'name': 'Valid Beer Name',
        'brewery': 'Valid Brewery',
        'description': 'A valid description.',
        'alcohol_content': '5.0',
        'beer_type': 'Pale Lager'
    }


class TestBeerOperations:
    def test_add_beer(self, client_with_admin, valid_beer_args):
        url = reverse("beer-list")
        response = client_with_admin.post(url, valid_beer_args, format="json")
        assert response.status_code == HTTP_201_CREATED
        assert response.data["name"] == valid_beer_args["name"]

    def test_add_beer_nonalcoholic_fails(self, client_with_admin, valid_beer_args):
        url = reverse("beer-list")
        invalid_args = {
            'name': 'Valid Beer Name',
            'brewery': 'Valid Brewery',
            'description': 'A valid description.',
            'alcohol_content': '0.6',
            'beer_type': 'Non-Alcoholic Beer'
        }
        response = client_with_admin.post(url, invalid_args, format="json")
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_add_beer_nonalcoholic_passes(self, client_with_admin, valid_beer_args):
        url = reverse("beer-list")
        invalid_args = {
            'name': 'Valid Beer Name',
            'brewery': 'Valid Brewery',
            'description': 'A valid description.',
            'alcohol_content': '0.5',
            'beer_type': 'Non-Alcoholic Beer'
        }
        response = client_with_admin.post(url, invalid_args, format="json")
        assert response.status_code == HTTP_201_CREATED

    def test_add_beer_alcoholfree_fails(self, client_with_admin, valid_beer_args):
        url = reverse("beer-list")
        invalid_args = {
            'name': 'Valid Beer Name',
            'brewery': 'Valid Brewery',
            'description': 'A valid description.',
            'alcohol_content': '0.1',
            'beer_type': 'Alcohol-Free Wheat Beer'
        }
        response = client_with_admin.post(url, invalid_args, format="json")
        assert response.status_code == HTTP_400_BAD_REQUEST

    def test_add_beer_alcoholfree_passes(self, client_with_admin, valid_beer_args):
        url = reverse("beer-list")
        invalid_args = {
            'name': 'Valid Beer Name',
            'brewery': 'Valid Brewery',
            'description': 'A valid description.',
            'alcohol_content': '0.0',
            'beer_type': 'Alcohol-Free Wheat Beer'
        }
        response = client_with_admin.post(url, invalid_args, format="json")
        assert response.status_code == HTTP_201_CREATED

    def test_edit_beer(self, client_with_admin, beer, valid_beer_args):
        url = reverse("beer-detail", args=[beer.id])
        valid_beer_args["name"] = "Updated Beer"
        response = client_with_admin.put(url, valid_beer_args, format="json")
        assert response.status_code == HTTP_200_OK
        assert response.data["name"] == "Updated Beer"

    def test_delete_beer(self, client_with_admin, beer):
        url = reverse("beer-detail", args=[beer.id])
        response = client_with_admin.delete(url)
        assert response.status_code == HTTP_204_NO_CONTENT


class TestBeerRetrieval:
    def test_retrieve_beer(self, client_with_user, beer):
        url = reverse("beer-detail", args=[beer.id])
        response = client_with_user.get(url)
        assert response.status_code == HTTP_200_OK
        assert response.data["name"] == beer.name

    def test_retrieve_beer_invalid_id(self, client_with_user):
        url = reverse("beer-detail", args=["invalidId"])
        response = client_with_user.get(url)
        assert response.status_code == HTTP_404_NOT_FOUND

    def test_retrieve_all_beers(self, client_with_user, beers):
        url = reverse("beer-list")
        response = client_with_user.get(url)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == len(beers)


class TestBeerRetrievalByName:
    def test_get_beer_by_exact_name(self, client_with_user, beer):
        url = reverse("beers:get-beer-by-name-path", kwargs={"beer_name": beer.name})
        response = client_with_user.get(url)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]["name"] == beer.name

    def test_get_beer_by_partial_name(self, client_with_user, beers):
        partial_name = "Beer"
        url = reverse("beers:get-beer-by-name-path", kwargs={"beer_name": partial_name})
        response = client_with_user.get(url)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == len(beers)
        for beer_data in response.data:
            assert partial_name in beer_data["name"]

    def test_get_beer_by_name_no_match(self, client_with_user):
        non_existent_name = "NonExistentBeer"
        url = reverse("beers:get-beer-by-name-path", kwargs={"beer_name": non_existent_name})
        response = client_with_user.get(url)
        assert response.status_code == HTTP_200_OK
        assert len(response.data) == 0

    def test_get_beer_by_name_as_unauthorized_user(self, client, beer):
        url = reverse("beers:get-beer-by-name-path", kwargs={"beer_name": beer.name})
        response = client.get(url)
        assert response.status_code == HTTP_403_FORBIDDEN


class TestUnauthorizedAccess:
    def test_add_beer_unauthenticated(self, client, valid_beer_args):
        url = reverse("beer-list")
        response = client.post(url, valid_beer_args, format="json")
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_access_endpoint_as_anonymous_user(self, client):
        url = reverse("beer-list")
        response = client.get(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_add_beer_as_standard_user(self, client_with_user, valid_beer_args):
        url = reverse("beer-list")
        response = client_with_user.post(url, valid_beer_args, format="json")
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_edit_beer_as_standard_user(self, client_with_user, beer, valid_beer_args):
        url = reverse("beer-detail", args=[beer.id])
        valid_beer_args["name"] = "Updated Beer"
        response = client_with_user.put(url, valid_beer_args, format="json")
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_delete_beer_as_standard_user(self, client_with_user, beer):
        url = reverse("beer-detail", args=[beer.id])
        response = client_with_user.delete(url)
        assert response.status_code == HTTP_403_FORBIDDEN

@pytest.fixture
def breweries(db):
    return [
        mixer.blend("beers.Beer", brewery="Brewery 1"),
        mixer.blend("beers.Beer", brewery="Brewery 2"),
        mixer.blend("beers.Beer", brewery="Brewery 1"),  # Duplicate brewery
    ]

class TestBreweryActions:
    def test_list_breweries(self, client_with_user, breweries):
        url = reverse("breweries:list-breweries")
        response = client_with_user.get(url)
        assert response.status_code == HTTP_200_OK
        # Check that the response contains only unique breweries
        assert set(response.data) == {"Brewery 1", "Brewery 2"}

    def test_list_breweries_unauthenticated(self, client, breweries):
        url = reverse("breweries:list-breweries")
        response = client.get(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_number_of_breweries(self, client_with_user, breweries):
        url = reverse("breweries:number-of-breweries")
        response = client_with_user.get(url)
        assert response.status_code == HTTP_200_OK
        # Check that the count of unique breweries is correct
        assert response.data["count"] == 2

    def test_number_of_breweries_unauthenticated(self, client, breweries):
        url = reverse("breweries:number-of-breweries")
        response = client.get(url)
        assert response.status_code == HTTP_403_FORBIDDEN

    def test_get_beers_by_brewery(self, client_with_user, breweries):
        url = reverse("breweries:get-beers-by-brewery", kwargs={"brewery_name": "Brewery 1"})
        response = client_with_user.get(url)
        assert response.status_code == HTTP_200_OK
        # Check that all beers belong to the specified brewery
        for beer in response.data:
            assert beer["brewery"] == "Brewery 1"

    def test_get_beers_by_brewery_no_beers(self, client_with_user):
        url = reverse("breweries:get-beers-by-brewery", kwargs={"brewery_name": "NonExistentBrewery"})
        response = client_with_user.get(url)
        assert response.status_code == HTTP_200_OK
        # Check that no beers are returned
        assert len(response.data) == 0

    def test_get_beers_by_brewery_unauthenticated(self, client, breweries):
        url = reverse("breweries:get-beers-by-brewery", kwargs={"brewery_name": "Brewery 1"})
        response = client.get(url)
        assert response.status_code == HTTP_403_FORBIDDEN