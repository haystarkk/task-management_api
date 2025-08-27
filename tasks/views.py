# tasks/views.py

from rest_framework import generics, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import Task
from .serializers import TaskSerializer
from .permissions import IsOwnerOrReadOnly

class TaskListCreateView(generics.ListCreateAPIView):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description']
    ordering_fields = ['due_date', 'priority']

    def get_queryset(self):
        return self.request.user.tasks.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]

    def get_queryset(self):
        return self.request.user.tasks.all()
    
    def perform_update(self, serializer):
        instance = self.get_object()
        if instance.status == 'Completed':
            return Response({"detail": "Cannot edit a completed task."}, status=status.HTTP_400_BAD_REQUEST)
        serializer.save()

@action(detail=True, methods=['patch'])
def toggle_complete(self, request, pk=None):
    task = self.get_object()
    if task.status == 'Completed':
        task.status = 'Pending'
        task.completed_at = None
    else:
        task.status = 'Completed'
        task.completed_at = timezone.now()
    task.save()
    serializer = self.get_serializer(task)
    return Response(serializer.data)