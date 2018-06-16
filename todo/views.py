# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, DeleteView, CreateView

from .forms import TaskForm
from .models import Task


# Create your views here.

class AbstractLogin(LoginRequiredMixin):
    login_url = '/login/'
    redirect_field_name = reverse_lazy('tasklist')

    class Meta:
        abstract = True


class TaskListView(AbstractLogin, ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        tasks = Task.objects.all()
        filtered_tasks = [tasks.filter(status="todo"), tasks.filter(status="in_progress"), tasks.filter(status="done")]
        context["tasks"] = filtered_tasks
        return context


class UpdateStatusView(AbstractLogin, DetailView):
    model = Task

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        task = Task.update_status(task)
        task.save()
        return redirect('tasklist')


class TaskDetailView(AbstractLogin, DetailView):
    model = Task
    template_name = "todo/task_detail.html"


class TaskFormView(AbstractLogin, FormView):
    form_class = TaskForm
    template_name = "todo/task_form.html"
    success_url = reverse_lazy("tasklist")

    def get_initial(self):
        self.initial['author'] = self.request.user
        return self.initial.copy()

    def form_valid(self, form):
        status = self.kwargs['string']
        form.save(status)
        return HttpResponseRedirect(self.get_success_url())


class DeleteTaskView(AbstractLogin, DeleteView):
    model = Task
    success_url = reverse_lazy("tasklist")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)


class SignupUserView(CreateView):
    form_class = UserCreationForm
    template_name = "registration/signup.html"
    success_url = reverse_lazy('tasklist')
