# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import redirect
from django.views.generic import ListView, DetailView

from .models import Task


# Create your views here.

class TaskListView(ListView):
    model = Task

    def get(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        if request.GET:
            id = request.GET['update']
            task = Task.objects.get(id=id)
            task = Task.update_status(task)
            task.save()
            return redirect('tasklist')
        context = self.get_context_data()
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        context = super(TaskListView, self).get_context_data(**kwargs)
        tasks = Task.objects.all()
        filtered_tasks = [tasks.filter(status="todo"), tasks.filter(status="in progress"), tasks.filter(status="done")]
        context["tasks"] = filtered_tasks
        return context


class TaskDetailView(DetailView):
    model = Task
    template_name = "todo/task_detail.html"
