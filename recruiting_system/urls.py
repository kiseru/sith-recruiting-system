from django.urls import path

from recruiting_system import views

urlpatterns = [
    path('siths/', views.SithListView.as_view(), name='sith_list'),
]
