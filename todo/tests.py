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
        Task.objects.create(title="First task", text="Some text about first task", status="todo")
        Task.objects.create(title="Second task", text="Some text about second task", status="in_progress")
        Task.objects.create(title="Third task", text="Some text about third task", status="done")
        self.f = RequestFactory()
        self.user = User.objects.create_user(username='tester', email='tester@jtester.com', password='top_secret')

    def test_should_display_correct_list(self):
        request = self.f.get(reverse('tasklist'))
        request.user = self.user
        v = setup_view(TaskListView(), request)
        v.object_list = Task.objects.all()
        data = v.get_context_data()

        self.assertTrue(data['tasks'])
        self.assertEqual([len(qs) for qs in data['tasks']], [1, 1, 1])

    def test_update_should_return_correct_record(self):
        request = self.f.get(reverse('updatestatus', kwargs={"pk": "1"}))
        request.user = self.user
        kwargs = {"pk": "1"}
        v = setup_view(UpdateStatusView(), request, **kwargs)
        v.get(v.request)
        task = Task.objects.get(id=1)
        self.assertEqual(task.status, "in_progress")

    def test_update_should_redirect(self):
        request = self.f.get(reverse('updatestatus', kwargs={"pk": "1"}))
        request.user = self.user
        kwargs = {"pk": "1"}
        v = setup_view(UpdateStatusView(), request, **kwargs)
        v.get(v.request)
        response = UpdateStatusView.as_view()(v.request, pk=1)
        self.assertEqual(response.status_code, 302)


class TestFormView(TestCase):

    def setUp(self):
        form_data = {"title": "First task", "text": "Some text about first task"}
        self.form = TaskForm(data=form_data)

    def test_form_should_pas_smoke_test(self):
        self.assertTrue(self.form.is_valid())

    def test_should_save_form_with_todo_status(self):
        status = "todo"
        form = self.form
        form.save(status)
        task = Task.objects.get(id=1)
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
        form.save(status)
        task = Task.objects.get(id=1)
        self.assertEqual(task.title, "First task")
        self.assertEqual(task.status, "done")


class TestModelFunctions(TestCase):

    def setUp(self):
        self.object = Task.objects.create(title="First task", text="Some text about first task", status="todo")

    def test_todo_should_change_to_in_progress(self):
        object = Task.update_status(self.object)
        self.assertEqual(object.status, "in_progress")

    def test_in_progress_should_change_to_done(self):
        self.object.status = "in_progress"
        object = Task.update_status(self.object)
        self.assertEqual(object.status, "done")

    def test_done_should_change_to_to_delete(self):
        self.object.status = "done"
        object = Task.update_status(self.object)
        self.assertEqual(object.status, "to_delete")
