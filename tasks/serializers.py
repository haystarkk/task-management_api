# tasks/serializers.py

from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Task
        fields = ('id', 'owner', 'title', 'description', 'due_date', 'priority', 'status', 'completed_at', 'created_at', 'updated_at')

    def validate_due_date(self, value):
        from datetime import date
        if value < date.today():
            raise serializers.ValidationError("Due date cannot be in the past.")
        return value

    def validate_status(self, value):
        if self.instance and self.instance.status == 'Completed' and self.instance.status != value:
            raise serializers.ValidationError("Cannot change status of a completed task directly.")
        return value