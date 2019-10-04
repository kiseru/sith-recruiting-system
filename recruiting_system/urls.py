from django.urls import path

from recruiting_system import views

urlpatterns = [
    path('recruits/new/', views.RecruitCreateView.as_view(), name='recruit_create'),
    path('recruits/<int:pk>/trial/', views.RecruitTrialView.as_view(), name='recruit_trial'),
    path('recruits/<int:pk>/', views.RecruitDetailView.as_view(), name='recruit_detail'),
    path('siths/<int:pk>', views.SithDetailView.as_view(), name='sith_detail'),
    path('siths/', views.SithListView.as_view(), name='sith_list'),
]
