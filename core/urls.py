from django.contrib.auth.decorators import login_required
from django.urls import path, reverse_lazy
from . import views

app_name = 'Core'

urlpatterns = [
    path('register-user', views.register_user, name='Register'),
    path('login-user', views.loginview, name='Login'),
    path('logout', login_required(views.logoutview, login_url=reverse_lazy('Core:Login')), name='Logout'),
    path('create-task', login_required(views.CreateTask.as_view(), login_url=reverse_lazy('Core:Login')),
         name='Create Task'),
    path('', login_required(views.TaskList.as_view(), login_url=reverse_lazy('Core:Login')), name='Task List'),
    path('delete-task-confirm/<pk>',
         login_required(views.DeleteConfirmView.as_view(), login_url=reverse_lazy('Core:Login')),
         name='Delete Confirm'),
    path('task-delete/<pk>', login_required(views.delete_task, login_url=reverse_lazy('Core:Login')),
         name='Task Delete'),
    path('task-detail/<pk>', login_required(views.TaskDetailView.as_view(), login_url=reverse_lazy('Core:Login')),
         name='Task Detail'),
    path('task-complete/<pk>', login_required(views.task_complete, login_url=reverse_lazy('Core:Login')),
         name='Task Complete'),
    path('search', login_required(views.ajax_search, login_url=reverse_lazy('Core:Login')), name='Search'),
    path('task-reorder/', login_required(views.TaskReorder.as_view(), login_url=reverse_lazy('Core:Login')),
         name='Task Reorder'),
    path('test', views.test, name='Test')
]
