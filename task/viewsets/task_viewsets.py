from rest_framework import viewsets
from ..models import Task
from ..serializers.task_serializers import TaskListSerializers, TaskRetrieveSerializers, TaskWriteSerializers

from task.utilities.pagination import MyPageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from task.utilities.permissions import taskPermission
from rest_framework.permissions import IsAuthenticated

class taskViewsets(viewsets.ModelViewSet):
    serializer_class = TaskListSerializers
    queryset = Task.objects.all().order_by('-id')
    pagination_class = MyPageNumberPagination
    permission_classes = [IsAuthenticated, taskPermission]

    filter_backends = [DjangoFilterBackend]
    
    filterset_fields = {
        'status' : ['exact'],
        'duedate' : ['exact', 'gte', 'lte'],
    }

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset
    
    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return TaskWriteSerializers
        elif self.action == 'retrieve':
            return TaskRetrieveSerializers
        return super().get_serializer_class()

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
class TaskStatusUpdateView(APIView):

    def patch(self, request, pk):
        try:
            task = Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return Response({'error': 'Task not found'}, status=status.HTTP_400_BAD_REQUEST)

        # Only admins or the assigned user can update status
        if not request.user.is_staff and task.assigned_to != request.user:
            return Response({'error': 'Not allowed'}, status=status.HTTP_403_FORBIDDEN)
        
        # Restriction: regular users cannot complete overdue tasks
        if not request.user.is_staff and task.duedate < timezone.now().date():
            return Response({
                'error': 'Cannot mark task as completed after due date without admin intervention.'
            }, status=status.HTTP_403_FORBIDDEN)
        
        task.status = 'completed'
        task.save()
        return Response({'message': 'Task marked as completed'}, status=status.HTTP_200_OK)