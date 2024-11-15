from django.urls import path
from .views import initiate_drone_task

urlpatterns = [
    path('task/initiate/', initiate_drone_task, name='initiate-drone-task'),
]
