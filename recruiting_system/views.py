from django.urls import reverse_lazy
from django.views import generic

from recruiting_system import models


class SithListView(generic.ListView):
    model = models.Sith


class RecruitCreateView(generic.CreateView):
    model = models.Recruit
    fields = (
        'name',
        'email',
        'age',
        'habitat_planet'
    )
    success_url = reverse_lazy('recruit_create')
