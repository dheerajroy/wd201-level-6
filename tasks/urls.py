from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import AllTasksView, DetailTaskView, CreateTaskView, UpdateTaskView, DeleteTaskView

urlpatterns = [
    path('', login_required(AllTasksView.as_view()), name='index'),
    path('<int:pk>/', DetailTaskView.as_view(), name='detail_task'),
    path('create/', CreateTaskView.as_view(), name='create_task'),
    path('update/<int:pk>/', UpdateTaskView.as_view(), name='update_task'),
    path('delete/<int:pk>/', DeleteTaskView.as_view(), name='delete_task')
]
