# tasks/urls.py

from django.urls import path
from .views import TaskListCreateView, TaskDetailView

urlpatterns = [
    # Endpoint to list all tasks and create a new task
    path('', TaskListCreateView.as_view(), name='task-list-create'),

    # Endpoint for a specific task (retrieve, update, delete)
    path('<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

    # You can add a specific endpoint for marking tasks as complete
    # For now, this is handled by a PUT/PATCH request to the detail view.
]