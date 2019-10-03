import uuid

from django.core import validators
from django.db import models


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
    code = models.SlugField(default=uuid.uuid4, editable=False, verbose_name='Идентификатор')

    class Meta:
        verbose_name = 'Испытание'
        verbose_name_plural = 'Испытания'

    def __str__(self):
        return str(self.code)


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


class RecruitAnswer(models.Model):
    question = models.ForeignKey(Question, models.PROTECT, verbose_name='Вопрос')
    answer = models.ForeignKey(Answer, models.PROTECT, verbose_name='Ответ')
    recruit = models.ForeignKey(Recruit, models.PROTECT, verbose_name='Рекрут')

    class Meta:
        verbose_name = 'Ответ рекрутера'
        verbose_name_plural = 'Ответ рекрутеров'
        unique_together = ('question', 'recruit')
