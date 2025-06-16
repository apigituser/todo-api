from django.urls import path
from . import views

urlpatterns = [
    path('todos/', views.create_paginate_handle),
    path('todos/<int:id>', views.update_delete_handle),
    path('register/', views.register),
    path('login/', views.loginUser),
]
