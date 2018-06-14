# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, FormView, DeleteView

from .forms import TaskForm
from .models import Task


# Create your views here.

class TaskListView(ListView):
    model = Task

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        tasks = Task.objects.all()
        filtered_tasks = [tasks.filter(status="todo"), tasks.filter(status="in_progress"), tasks.filter(status="done")]
        context["tasks"] = filtered_tasks
        return context


class UpdateStatusView(DetailView):
    model = Task

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        task = Task.update_status(task)
        task.save()
        return redirect('tasklist')


class TaskDetailView(DetailView):
    model = Task
    template_name = "todo/task_detail.html"


class TaskFormView(FormView):
    form_class = TaskForm
    template_name = "todo/task_form.html"
    success_url = reverse_lazy("tasklist")

    def form_valid(self, form):
        status = self.kwargs['string']
        form.save(status)
        return HttpResponseRedirect(self.get_success_url())


class DeleteTaskView(DeleteView):
    model = Task
    success_url = reverse_lazy("tasklist")

    def get(self, *args, **kwargs):
        return self.post(*args, **kwargs)
