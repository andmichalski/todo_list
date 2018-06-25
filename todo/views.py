# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from collections import defaultdict

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, CreateView, UpdateView
from django.views.generic.edit import DeletionMixin

from .forms import TaskForm, TaskUpdateForm
from .models import Task


# Create your views here.

class LoginView(LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = reverse_lazy('tasklist')


class TaskListView(LoginView, ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        tasks_by_status = defaultdict(list)
        for task in Task.objects.all().exclude(status="to_delete"):
            tasks_by_status[task.status].append(task)
        context.update(tasks_by_status)
        return context


class UpdateStatusView(LoginView, UpdateView):
    model = Task
    template_name_suffix = '_update_form'
    success_url = reverse_lazy('tasklist')
    form_class = TaskUpdateForm


class TaskDetailView(LoginView, DetailView):
    model = Task
    template_name = "todo/task_detail.html"


class TaskFormView(LoginView, FormView):
    form_class = TaskForm
    template_name = "todo/task_form.html"
    success_url = reverse_lazy("tasklist")

    def get_initial(self):
        initial = super(TaskFormView, self).get_initial()
        initial['author'] = self.request.user
        initial['status'] = self.kwargs['status']
        return initial

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.get_success_url())


class DeleteTaskView(LoginView, DeletionMixin, DetailView):
    model = Task
    success_url = reverse_lazy("tasklist")


class SignupUserView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('tasklist')
