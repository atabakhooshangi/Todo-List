from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.views import View
from django.views.generic import CreateView, ListView, DeleteView, TemplateView, DetailView
from django.views.decorators.csrf import csrf_exempt
from .forms import RegisterForm, LoginForm, TaskForm, PositionForm
from django.contrib.auth import (
    authenticate, get_user_model, password_validation,
)
from django.db import transaction
from .models import Task

User = get_user_model()


def home(request):
    return render(request, 'login.html', {})


def register_user(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST or None)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            check_user = User.objects.filter(username=username)
            if check_user.exists():
                form.add_error(request, 'Invalid username')
            else:
                user = form.save()
                user.set_password(form.cleaned_data['password'])
                user.save()
                return redirect(reverse('Core:Task List'))

    form = RegisterForm(request.POST or None)
    context = {
        'form': form
    }
    return render(request, 'register.html', context)


def loginview(request):
    if request.user.is_authenticated:
        return redirect('Core:Task List')
    form = LoginForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None:
                login(request, user)
                return redirect(reverse('Core:Task List'))
            else:
                form.add_error('username', 'Invalid credentials')

    context = {
        'form': form
    }
    return render(request, 'login.html', context)


def logoutview(request):
    logout(request)
    return redirect('Core:Login')


class CreateTask(CreateView):
    form_class = TaskForm
    model = Task
    template_name = 'task_form.html'
    success_url = reverse_lazy('Core:Task List')

    def form_valid(self, form):
        task = form.instance
        task.user = self.request.user
        task.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateTask, self).get_context_data()
        context['form'] = self.form_class
        return context


class TaskList(ListView):
    template_name = 'task_list.html'

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(TaskList, self).get_context_data()
        incomplete_tasks = Task.objects.filter(user=self.request.user, complete=False)
        context['count'] = incomplete_tasks.count()
        return context


class DeleteConfirmView(TemplateView):
    template_name = 'task_confirm_delete.html'

    def get_context_data(self, **kwargs):
        context = super(DeleteConfirmView, self).get_context_data()
        task = get_object_or_404(Task, id=self.kwargs['pk'])
        context['task'] = task
        return context


def delete_task(request, pk):
    task = get_object_or_404(Task, id=pk)
    task.delete()
    return redirect('Core:Task List')


class TaskDetailView(DetailView):
    template_name = 'task.html'
    context_object_name = 'task'

    def get_queryset(self, *args, **kwargs):
        return Task.objects.filter(id=self.kwargs['pk'])


def task_complete(request, pk):
    task = get_object_or_404(Task, id=pk)
    if task.complete:
        task.complete = False
    else:
        task.complete = True
    task.save()
    return redirect('Core:Task List')


@csrf_exempt
def ajax_search(request):
    query = request.POST.get('query')
    filtered_tasks = Task.objects.search(query=query)
    filtered_tasks = filtered_tasks.filter(user=request.user)
    # for i in range(1, 25):
    #     task = Task.objects.create(title=f'test{i}', description='any', user=request.user)
    #     task.save()
    tmp = render_to_string('ajax-search.html', {'tasks': filtered_tasks})
    return JsonResponse({'data': tmp})


class TaskReorder(View):
    def post(self, request):
        form = PositionForm(request.POST)

        if form.is_valid():
            positionList = form.cleaned_data["position"].split(',')
            print(positionList)

            with transaction.atomic():
                self.request.user.set_task_order(positionList)

        return redirect(reverse_lazy('Core:Task List'))


def test(request):
    return render(request, '404.html', {})
