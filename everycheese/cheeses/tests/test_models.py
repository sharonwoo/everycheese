import pytest
from ..models import Cheese  # import cheese model class for testing
from .factories import CheeseFactory

pytestmark = pytest.mark.django_db


def test___str__():
    cheese = CheeseFactory()

    # test get_absolute_url
    url = cheese.get_absolute_url()
    assert url == f"/cheeses/{cheese.slug}/"

    # test str
    assert cheese.__str__() == cheese.name
    assert str(cheese) == cheese.name

    # cheese = Cheese.objects.create(
    #                     name="Stracchino",
    #                     description="Semi-sweet cheese that goes well with starches.",
    #                     firmness=Cheese.Firmness.SOFT,
    #                     )
    # assert cheese.__str__() == "Stracchino"
    # assert str(cheese) == "Stracchino"
