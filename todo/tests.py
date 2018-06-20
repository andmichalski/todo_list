# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import factory
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.test import TestCase, RequestFactory

from .forms import TaskForm, TaskUpdateForm
from .models import Task
from .views import TaskListView, TaskDetailView, UpdateStatusView, TaskFormView

# Create your tests here.

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User
        django_get_or_create = ('username',)

    username = 'tester'
    email = 'tester@jtester.com'
    password = 'top_secret'

class TaskFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Task

    title = factory.Sequence(lambda n: 'Title_{}'.format(n))
    text = factory.Sequence(lambda n: 'some_text_{}'.format(n))
    status = factory.Iterator([Task.TODO, Task.IN_PROGRESS, Task.DONE, Task.TO_DELETE])
    author = factory.SubFactory(UserFactory, username='tester')

class TodoViewsTests(TestCase):

    def setUp(self):
        self.f = RequestFactory()
        self.user = UserFactory()
        self.task0, self.task1,self. task2, self.task3,= [TaskFactory() for i in range(4)]

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
        self.assertFalse(response.context_data["to_delete"])

    def test_detail_view_should_display_correct_record(self):
        request = self.f.get(reverse('taskdetail', kwargs={'pk': "1"}))
        request.user = self.user
        view = TaskDetailView.as_view()
        kwargs = {'pk': "1"}
        response = view(request, **kwargs)
        response.render()
        self.assertTrue(response.context_data['object'])
        self.assertEqual(response.context_data['object'].text, "some_text_0")


    def test_update_view_should_update_correct_record(self):
        request = self.f.get(reverse('updatestatus', kwargs={"pk": "1"}))
        request.user = self.user
        form_data = {"status": "in_progress"}
        request.form = TaskUpdateForm(instance=self.task0, data=form_data)
        self.assertTrue(request.form.is_valid())

        request.form.save()
        kwargs = {"pk": "1"}
        view = UpdateStatusView.as_view()
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.task0.status, "in_progress")


    def test_task_form_view_should_create_correct_record(self):
        request = self.f.get(reverse('taskform', kwargs={"status": "todo"}))
        request.user = self.user
        form_data = {"title": "next_title", "text":"more text"}
        request.form = TaskForm(data=form_data)
        kwargs = {"status": "todo"}
        view = TaskFormView.as_view()
        response = view(request, **kwargs)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.context_data['form'].initial, {"status": "todo", "author": UserFactory()})

    def test_form_task_should_be_valid_and_save_record(self):
        request = self.f.get(reverse('taskform', kwargs={"status": "todo"}))
        request.user = self.user
        form_data = {"title": "next_title", "text": "more text", "status": "todo", "author": self.user}
        request.form = TaskForm(data=form_data)
        self.assertTrue(request.form.is_valid())

        form.save()
        self.assertEqual(Task.objects.count(), 5)


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

class FormsTest(TodoViewsTests):


    def test_update_form_should_be_valid(self):
        form_data = {"status": "in_progress"}
        form = TaskUpdateForm(instance=self.task0, data=form_data)
        self.assertTrue(form.is_valid())

    def test_should_save_record(self):
        form_data = {"status": "in_progress"}
        form = TaskUpdateForm(instance=self.task0, data=form_data)
        form.save()
        self.assertEqual(self.task0.status, "in_progress")