from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('toggle/<int:task_id>/', views.toggle_task, name='toggle'),
    path('delete/<int:task_id>/', views.delete_task, name='delete'),
]
