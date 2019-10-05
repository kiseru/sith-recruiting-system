from django.core.mail import send_mail
from django.db.models import Count
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import generic

from recruiting_system import models


class SithListView(generic.ListView):
    model = models.Sith
    queryset = models.Sith.objects.annotate(Count('recruit')).select_related('learning_planet')


class RecruitCreateView(generic.CreateView):
    model = models.Recruit
    fields = (
        'name',
        'email',
        'age',
        'habitat_planet'
    )

    def get_success_url(self):
        return reverse_lazy('recruit_trial', kwargs={'pk': self.object.pk})


class RecruitTrialView(generic.DetailView,
                       generic.FormView):
    model = models.Recruit
    template_name = 'recruiting_system/recruit_trial.html'

    def get_context_data(self, **kwargs):
        kwargs['questions'] = models.Trial.objects.first().question_set.all().prefetch_related('answer_set')
        return kwargs

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.recruitanswer_set.exists():
            return redirect('recruit_create')
        context = self.get_context_data(object=self.object)
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        answers = [(int(question_id), int(answer_id)) for question_id, answer_id in request.POST.items()
                   if question_id != 'csrfmiddlewaretoken']
        for question_id, answer_id in answers:
            models.RecruitAnswer.objects.create(question_id=question_id, answer_id=answer_id, recruit_id=kwargs['pk'])
        return redirect(reverse_lazy('recruit_trial', kwargs={'pk': kwargs['pk']}))


class SithDetailView(generic.DetailView,
                     generic.FormView):
    model = models.Sith
    template_name = 'recruiting_system/sith_detail.html'
    queryset = models.Sith.objects.annotate(Count('recruit'))

    def get_context_data(self, **kwargs):
        kwargs['recruits'] = models.Recruit.objects.filter(
            sith__isnull=True,
            recruitanswer__isnull=False
        ).select_related('habitat_planet')
        return kwargs

    def post(self, request, *args, **kwargs):
        sith_id = kwargs['pk']
        sith = models.Sith.objects.annotate(Count('recruit')).get(pk=sith_id)
        if sith.recruit__count >= 3:
            context = {
                **self.get_context_data(),
                'object': sith,
                'error': 'У вас не может быть больше трех Рук Тени'
            }
            return render(request, self.template_name, context)

        recruit = models.Recruit.objects.get(pk=request.POST['recruit_id'])
        recruit.sith_id = sith_id
        recruit.save()
        send_mail(
            'Вы теперь Рука Тени',
            f'{recruit.name}, Вы теперь Рука Тени. {sith} выбрал Вас',
            'sith_recruiting_system@test.com',
            (recruit.email,)
        )
        return redirect(reverse_lazy('sith_detail', kwargs={'pk': sith_id}))


class RecruitDetailView(generic.DetailView):
    model = models.Recruit
    queryset = models.Recruit.objects.select_related('habitat_planet')

    def get_context_data(self, **kwargs):
        kwargs['answers'] = models.RecruitAnswer.objects.select_related(
            'question',
            'answer',
        ).filter(recruit_id=kwargs['object'].pk)
        return kwargs


class SithHasMoreThanOneRecruitListView(SithListView):
    def get_queryset(self):
        return self.queryset.filter(recruit__count__gt=1)


class RootRedirectView(generic.RedirectView):
    pattern_name = 'sith_list'
