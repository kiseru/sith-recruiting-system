from django.core import validators
from django.db import models
from django.db.models import Q, F


class Planet(models.Model):
    name = models.CharField(max_length=30, verbose_name='Название')

    class Meta:
        verbose_name = 'Планета'
        verbose_name_plural = 'Планеты'

    def __str__(self):
        return self.name


class Recruit(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    habitat_planet = models.ForeignKey(Planet, models.PROTECT, verbose_name='Планета обитания')
    age = models.PositiveSmallIntegerField(
        verbose_name='Возраст',
        validators=(validators.MinValueValidator(0), validators.MaxValueValidator(130))
    )
    email = models.EmailField(verbose_name='E-mail')
    sith = models.ForeignKey('Sith', models.PROTECT, verbose_name='Ситх', null=True, blank=True)

    class Meta:
        verbose_name = 'Рекрут'
        verbose_name_plural = 'Рекруты'

    def __str__(self):
        return self.name


class Sith(models.Model):
    name = models.CharField(max_length=30, verbose_name='Имя')
    learning_planet = models.ForeignKey(Planet, models.PROTECT, verbose_name='Планета обучения')

    class Meta:
        verbose_name = 'Ситх'
        verbose_name_plural = 'Ситхи'

    def __str__(self):
        return self.name


class Trial(models.Model):
    pass

    class Meta:
        verbose_name = 'Испытание'
        verbose_name_plural = 'Испытания'


class Question(models.Model):
    question = models.TextField(verbose_name='Вопрос')
    trial = models.ForeignKey(Trial, models.PROTECT, verbose_name='Испытание')

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'

    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.TextField(verbose_name='Ответ')
    question = models.ForeignKey(Question, models.PROTECT, verbose_name='Вопрос')
    is_correct = models.BooleanField(verbose_name='Правилный', default=False)

    class Meta:
        verbose_name = 'Ответ'
        verbose_name_plural = 'Ответы'

    def __str__(self):
        return self.answer


class Result(models.Model):
    recruit = models.ForeignKey(Recruit, models.PROTECT, verbose_name='Ректрут')

    class Meta:
        verbose_name = 'Результат'
        verbose_name_plural = 'Результаты'

    def __str__(self):
        return self.recruit


class RecruitAnswer(models.Model):
    question = models.ForeignKey(Question, models.PROTECT, verbose_name='Вопрос')
    result = models.ForeignKey(Result, models.PROTECT, verbose_name='Результат')
    answer = models.ForeignKey(Answer, models.PROTECT, verbose_name='Ответ')

    class Meta:
        verbose_name = 'Ответ рекрутера'
        verbose_name_plural = 'Ответ рекрутеров'
