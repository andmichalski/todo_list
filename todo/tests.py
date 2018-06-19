# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.shortcuts import reverse
from django.test import TestCase, RequestFactory

from .forms import TaskForm
from .models import Task
from .views import TaskListView, UpdateStatusView


# Create your tests here.

def setup_view(view, request, *args, **kwargs):
    view.request = request
    view.args = args
    view.kwargs = kwargs
    return view


class TaskViewTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='tester', email='tester@jtester.com', password='top_secret')
        Task.objects.create(title="First task", text="Some text about first task", status="todo", author=self.user)
        Task.objects.create(title="Second task", text="Some text about second task", status="in_progress",
                            author=self.user)
        Task.objects.create(title="Third task", text="Some text about third task", status="done", author=self.user)
        self.f = RequestFactory()

    def test_should_display_correct_list(self):
        request = self.f.get(reverse('tasklist'))
        request.user = self.user
        view = TaskListView.as_view()
        response = view(request)
        response.render()
        self.assertTrue(response.context_data["todo"])
        self.assertTrue(response.context_data["in_progress"])
        self.assertTrue(response.context_data["done"])
        self.assertEqual(len(response.context_data["todo"]), 1)
        self.assertEqual(len(response.context_data["in_progress"]), 1)
        self.assertEqual(len(response.context_data["done"]), 1)

    def test_update_should_return_correct_record(self):
        request = self.f.get(reverse('updatestatus', kwargs={"pk": "1"}))
        request.user = self.user
        kwargs = {"pk": "1"}
        view = UpdateStatusView.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 302)

        task = Task.objects.get(id=1)
        self.assertEqual(task.status, "in_progress")


class TestFormView(TestCase):

    def setUp(self):
        User.objects.create_user(username='tester', email='tester@jtester.com', password='top_secret')
        form_data = {"title": "First task", "text": "Some text about first task", "author": "1"}
        self.form = TaskForm(data=form_data)

    def test_form_should_be_valid(self):
        self.assertTrue(self.form.is_valid())

    def test_should_save_form_with_todo_status(self):
        status = "todo"
        form = self.form
        task = form.save(status)
        self.assertEqual(task.title, "First task")
        self.assertEqual(task.status, "todo")

    def test_should_save_form_with_in_progress_status(self):
        status = "in_progress"
        form = self.form
        form.save(status)
        task = Task.objects.get(id=1)
        self.assertEqual(task.title, "First task")
        self.assertEqual(task.status, "in_progress")

    def test_should_save_form_with_done_status(self):
        status = "done"
        form = self.form
        task = form.save(status)
        self.assertEqual(task.title, "First task")
        self.assertEqual(task.status, "done")


class TestModelFunctions(TestCase):

    def setUp(self):
        author = User.objects.create_user(username='tester', email='tester@jtester.com', password='top_secret')
        self.object = Task.objects.create(title="First task", text="Some text about first task", status="todo",
                                          author=author)

    def test_todo_should_change_to_in_progress(self):
        self.object.update_status()
        self.assertEqual(self.object.status, "in_progress")

    def test_in_progress_should_change_to_done(self):
        self.object.status = "in_progress"
        self.object.update_status()
        self.assertEqual(self.object.status, "done")

    def test_done_should_change_to_to_delete(self):
        self.object.status = "done"
        self.object.update_status()
        self.assertEqual(self.object.status, "to_delete")
