from todolist.authorization import IsOwnerPermission
from rest_framework.permissions import AllowAny
from todolist.serializers import UserSerializer, TaskSerializer, TaskCreateSerializer, UserCreateSerializer
from todolist.models import User, Task
from rest_framework.generics import ListCreateAPIView, ListAPIView, RetrieveUpdateDestroyAPIView



class UserList(ListCreateAPIView):
    """
    List all users, or create a new user.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


    def get_serializer(self, *args, **kwargs):
        self.serializer_class = UserSerializer
        if self.request.method == 'POST':
            self.serializer_class = UserCreateSerializer
        return super().get_serializer(*args, **kwargs)

class UserDetail(RetrieveUpdateDestroyAPIView):
    """
    Retrieve User details
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsOwnerPermission]

class UserTasksList(ListCreateAPIView):
    """
    List all users task, or create a new user task
    """
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerPermission]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        queryset = Task.objects.filter(user_id=user_id)
        return queryset
    
    def get_serializer(self, *args, **kwargs):
        self.serializer_class = TaskSerializer
        if self.request.method == 'POST':
            self.serializer_class = TaskCreateSerializer
        return super().get_serializer(*args, **kwargs)


class UserTasksDetail(RetrieveUpdateDestroyAPIView):
    """
    Retrieve Task details
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    lookup_field = 'id'
    permission_classes = [IsOwnerPermission]


class UserTasksSearch(ListAPIView):
    """
    Retrieve Tasks that matches date or title content
    """
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsOwnerPermission]

    def get_queryset(self):
        user_id = self.kwargs.get('pk')
        queryset = Task.objects.filter(user_id=user_id)

        title = self.request.query_params.get('title')
        if title:
            queryset = queryset.filter(title__icontains=title)
        date = self.request.query_params.get('date')
        if date:
            queryset = queryset.filter(date=date)
        
        
        return queryset