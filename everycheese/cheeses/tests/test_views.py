import pytest
from pytest_django.asserts import assertContains, assertRedirects
from django.urls import reverse
from django.contrib.sessions.middleware import SessionMiddleware
from django.test import RequestFactory as rf  # technically no need to alias
from everycheese.users.models import User
from ..models import Cheese
from ..views import CheeseCreateView, CheeseListView, CheeseDetailView
from .factories import CheeseFactory


pytestmark = pytest.mark.django_db


def test_good_cheese_list_view(rf):
    # Get the request
    request = rf.get(reverse("cheeses:list"))
    # Use the request to get the response
    response = CheeseListView.as_view()(request)
    # Test that the response is valid
    assertContains(response, "Cheese List")


def test_good_cheese_detail_view(rf):
    # Order some cheese from the CheeseFactory
    cheese = CheeseFactory()
    # Make a request for our new cheese
    request = rf.get(reverse("cheeses:detail", kwargs={"slug": cheese.slug}))
    # Use the request to get the response
    response = CheeseDetailView.as_view()(request, slug=cheese.slug)
    # Test that the response is valid
    assertContains(response, cheese.name)


def test_good_cheese_create_view(rf, admin_user):
    # Order some cheese from the CheeseFactory
    cheese = CheeseFactory()
    # Make a request for our new cheese
    request = rf.get(reverse("cheeses:add"))
    # Add an authenticated user
    request.user = admin_user
    # Use the request to get the response
    response = CheeseCreateView.as_view()(request)
    # Test that the response is valid
    assert response.status_code == 200


def test_cheese_list_contains_2_cheeses(rf):
    # Let's create a couple cheeses
    cheese1 = CheeseFactory()
    cheese2 = CheeseFactory()
    # Create a request and then a response # for a list of cheeses
    request = rf.get(reverse("cheeses:list"))
    response = CheeseListView.as_view()(request)
    # Assert that the response contains both cheese names # in the template.
    assertContains(response, cheese1.name)
    assertContains(response, cheese2.name)


def test_detail_contains_cheese_data(rf):
    cheese = CheeseFactory()
    # Make request for new cheese
    url = reverse("cheeses:detail", kwargs={"slug": cheese.slug})
    request = rf.get(url)
    response = CheeseDetailView.as_view()(request, slug=cheese.slug)
    assertContains(response, cheese.name)
    assertContains(response, cheese.get_firmness_display())
    assertContains(response, cheese.country_of_origin.name)


def test_cheese_create_form_valid(rf, admin_user):
    form_data = {
        "name": "Paski Sir",
        "description": "A salty hard cheese",
        "firmness": Cheese.Firmness.HARD,
    }
    request = rf.post(reverse("cheeses:add"), form_data)
    request.user = admin_user
    response = CheeseCreateView.as_view()(request)

    cheese = Cheese.objects.get(name="Paski Sir")

    assert cheese.description == "A salty hard cheese"
    assert cheese.firmness == Cheese.Firmness.HARD
    assert cheese.creator == admin_user