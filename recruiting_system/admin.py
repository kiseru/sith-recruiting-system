from django.contrib import admin

from recruiting_system import models


@admin.register(models.Planet)
class PlanetAdmin(admin.ModelAdmin):
    pass


@admin.register(models.Recruit)
class RecruitAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'age', 'habitat_planet', 'view_sith')

    def view_sith(self, obj):
        return obj.sith

    view_sith.empty_value_display = 'Нет мастера'


@admin.register(models.Sith)
class SithAdmin(admin.ModelAdmin):
    list_display = ('name', 'learning_planet')
    empty_value_display = '+++'


class QuestionInline(admin.TabularInline):
    model = models.Question


@admin.register(models.Trial)
class TrialAdmin(admin.ModelAdmin):
    inlines = (QuestionInline,)


class AnswerInline(admin.TabularInline):
    model = models.Answer


@admin.register(models.Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question',)
    inlines = (AnswerInline,)


@admin.register(models.Answer)
class AnswerAdmin(admin.ModelAdmin):
    list_display = ('answer', 'question')
