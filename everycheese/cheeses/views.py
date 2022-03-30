from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView
from .models import Cheese


class CheeseListView(ListView):
    model = Cheese


class CheeseDetailView(DetailView):
    model = Cheese


class CheeseCreateView(
    LoginRequiredMixin, CreateView
):  # remember to define get_absolute_url in model
    model = Cheese
    fields = ["name", "description", "firmness", "country_of_origin"]
