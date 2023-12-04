from django.urls import path
from . import views

# 04/12/2023 - Geoffroy
# URLs pour le gestionnaire de tâches V2

urlpatterns = [
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('status/<int:task_id>/<str:new_status>/', views.update_status, name='update_status'),
    path('delete/<int:task_id>/', views.delete_task, name='delete'),
    path('subtask/<int:parent_id>/', views.add_subtask, name='add_subtask'),
]
