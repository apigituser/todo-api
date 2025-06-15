from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.create_todo),
    path('todos/<int:id>', views.update_and_delete_todo),
    path('register/', views.register),
    path('login/', views.loginUser),
]
