import pytest
from ..models import Cheese # import cheese model class for testing

pytestmark = pytest.mark.django_db

def test___str__():
    cheese = Cheese.objects.create(
                        name="Stracchino", 
                        description="Semi-sweet cheese that goes well with starches.",
                        firmness=Cheese.Firmness.SOFT,
                        ) 
    assert cheese.__str__() == "Stracchino" 
    assert str(cheese) == "Stracchino"