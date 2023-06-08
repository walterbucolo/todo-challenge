from django.urls import include, path
from django.contrib import admin
from rest_framework.authtoken import views


urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('', include('todolist.urls')),
]