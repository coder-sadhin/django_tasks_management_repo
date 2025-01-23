from django.urls import path
from tasks.views import delete_task, manager_dashboard, update_task, user_dashboard, test, create_task, view_task

urlpatterns = [
    path('manager-dashboard/', manager_dashboard, name="manager_dashboard"),
    path('user-dashboard/', user_dashboard),
    path('test/', test),
    path('create-task/', create_task,name="create-task"),
    path('view-task/', view_task),
    path('update-task/<int:id>/', update_task, name="update-task"),
    path('delete-task/<int:id>/', delete_task, name="delete-task")
]