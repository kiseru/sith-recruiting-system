from django.views import generic

from recruiting_system import models


class SithListView(generic.ListView):
    model = models.Sith
