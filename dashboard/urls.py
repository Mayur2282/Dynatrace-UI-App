from django.contrib import admin
from django.urls import path
from dashboard import views


urlpatterns = [
    path('', views.index, name='index'),
    path('daily-activity', views.daily_activity, name='daily_activity'),
    path('problem-data', views.problem_data, name='problem_data'),
    path('user-management', views.user_management, name='user_management'),
]

