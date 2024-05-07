from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from .models import Task
from .serializers import TaskSerializer

class TaskListApiView(APIView):

    # 1. List all tasks
    def get(self, request, *args, **kwargs):
        '''
        List all the tasks for the authenticated user
        '''
        # tasks = Task.objects.filter(user=request.user)
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 2. Create a task
    def post(self, request, *args, **kwargs):
        '''
        Create a task with the given task data
        '''
        data = {
            'title': request.data.get('title'), 
            'description': request.data.get('description'), 
            'deadline': request.data.get('deadline')
        }
        serializer = TaskSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class TaskDetailApiView(APIView):

    def get_object(self, task_id):
        '''
        Helper method to get the object with given task_id and user_id
        '''
        try:
            return Task.objects.get(id=task_id)
        except Task.DoesNotExist:
            return None

    # Retrieve a task
    def get(self, request, task_id, *args, **kwargs):
        '''
        Retrieves the Task with given task_id
        '''
        print("Masuk ------------------------------------------------------- GET")
        task_instance = self.get_object(task_id)
        if not task_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = TaskSerializer(task_instance)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # Update a task
    def put(self, request, task_id, *args, **kwargs):
        '''
        Updates the task with given task_id if exists
        '''
        task_instance = self.get_object(task_id)
        data = {
            'title': request.data.get('title'), 
            'description': request.data.get('description'), 
            'deadline': request.data.get('deadline')
        }
        serializer = TaskSerializer(instance=task_instance, data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # Delete a task
    def delete(self, request, task_id, *args, **kwargs):
        '''
        Deletes the task with given task_id if exists
        '''
        print("Masuk ------------------------------------------------------- DELETE")
        task_instance = self.get_object(task_id)
        if not task_instance:
            return Response(
                {"res": "Object with todo id does not exists"},
                status=status.HTTP_400_BAD_REQUEST
            )
        task_instance.delete()
        return Response({"res": "Task deleted!"}, status=status.HTTP_200_OK)
