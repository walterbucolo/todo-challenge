from django.urls import path
from . import views


urlpatterns = [
    path('users/', views.UserList.as_view()), #List or create User
    path('users/<int:pk>/', views.UserDetail.as_view()), # Detail User
    path('users/<int:pk>/tasks/', views.UserTasksList.as_view()), # List tasks
    path('users/<int:pk>/tasks/<int:id>', views.UserTasksDetail.as_view()), # Detail task
    path('users/<int:pk>/tasks/search/', views.UserTasksSearch.as_view()), # Detail task
]