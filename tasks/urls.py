from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('health/', views.health, name='health'),
    path('about/', views.about, name='about'),
    path('tasks/', views.task_list, name='task-list'),
    path('tasks/<int:id>/', views.task_detail, name='task-detail'),
    path('echo/', views.echo, name='echo'),
]
