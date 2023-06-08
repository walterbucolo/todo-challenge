from rest_framework import serializers
from todolist.models import User, Task, Status


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
    
    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user


class TaskSerializer(serializers.ModelSerializer):
    status = serializers.CharField(source='get_status_display')

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'date', 'status', 'user']


class TaskCreateSerializer(serializers.ModelSerializer):
    status = serializers.ChoiceField(choices=Status.choices)

    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'date', 'status']
    
    def create(self, validated_data):
        validated_data['user_id'] = self.context['view'].kwargs.get('pk')
        return super().create(validated_data)