from django.shortcuts import redirect
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

    def get_success_url(self):
        return reverse_lazy('recruit_detail', kwargs={'pk': self.object.pk})


class RecruitDetailView(generic.DetailView,
                        generic.FormView):
    model = models.Recruit

    def get_context_data(self, **kwargs):
        kwargs['questions'] = models.Trial.objects.first().question_set.all()
        return kwargs

    def get(self, request, *args, **kwargs):
        if models.Recruit.objects.get(pk=kwargs['pk']).recruitanswer_set.exists():
            return redirect('recruit_create')

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        answers = [(int(question_id), int(answer_id)) for question_id, answer_id in request.POST.items()
                   if question_id != 'csrfmiddlewaretoken']
        for question_id, answer_id in answers:
            models.RecruitAnswer.objects.create(question_id=question_id, answer_id=answer_id, recruit_id=kwargs['pk'])
        return redirect(reverse_lazy('recruit_detail', kwargs={'pk': kwargs['pk']}))
