# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import reverse
from django.test import TestCase, RequestFactory

from .factories import TaskFactory, UserFactory
from .forms import TaskForm
from .models import Task
from .views import TaskListView, TaskDetailView, UpdateStatusView, TaskFormView, DeleteTaskView, SignupUserView


# Create your tests here.


class TodoViewsTests(TestCase):

    def setUp(self):
        self.f = RequestFactory()
        self.user = UserFactory()
        self.task0, self.task1, self.task2, self.task3 = [TaskFactory() for i in range(4)]

    def tearDown(self):
        TaskFactory.reset_sequence(0)

    def test_should_display_correct_list(self):
        request = self.f.get(reverse('tasklist'))
        request.user = self.user
        view = TaskListView.as_view()
        response = view(request)
        self.assertTrue(response.context_data["todo"])
        self.assertTrue(response.context_data["in_progress"])
        self.assertTrue(response.context_data["done"])
        self.assertEqual(len(response.context_data["todo"]), 1)
        self.assertEqual(len(response.context_data["in_progress"]), 1)
        self.assertEqual(len(response.context_data["done"]), 1)
        with self.assertRaises(KeyError):
            response.context_data["to_delete"]

    def test_detail_view_should_display_correct_record(self):
        request = self.f.get(reverse('taskdetail', kwargs={'pk': "1"}))
        request.user = self.user
        view = TaskDetailView.as_view()
        kwargs = {'pk': "1"}
        response = view(request, **kwargs)
        self.assertTrue(response.context_data['object'])
        self.assertEqual(response.context_data['object'].text, "some_text_0")

    def test_update_view_should_update_correct_record(self):
        request = self.f.post(reverse('updatestatus', kwargs={"pk": "1"}), data={"status": "in_progress"})
        request.user = self.user
        view = UpdateStatusView.as_view()
        response = view(request, pk=1)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Task.objects.get(pk=1).status, "in_progress")

    def test_task_form_view_should_have_correct_initial_values(self):
        request = self.f.get(reverse('taskform', kwargs={"status": "todo"}))
        request.user = self.user
        kwargs = {"status": "todo"}
        view = TaskFormView.as_view()
        response = view(request, **kwargs)
        self.assertTrue(response.status_code, 200)
        self.assertEqual(response.context_data['form'].initial, {"status": "todo", "author": UserFactory()})

    def test_delete_should_delete_selected_task(self):
        request = self.f.post(reverse('deletetask', kwargs={"pk": "1"}))
        request.user = self.user
        view = DeleteTaskView.as_view()
        kwargs = {"pk": "1"}
        response = view(request, **kwargs)
        self.assertEqual(response.status_code, 302)
        with self.assertRaises(ObjectDoesNotExist):
            Task.objects.get(pk=1)

    def test_signup_view_should_redirect_to_correct_template(self):
        request = self.f.get(reverse('signupview'))
        view = SignupUserView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["registration/signup.html"])
        self.assertContains(response, "Register")

    def test_user_not_authorized_should_be_redirect_to_login_page(self):
        request = self.f.get(reverse('tasklist'), follow=True)
        view = LoginView.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.template_name, ["registration/login.html"])
        self.assertContains(response, "login")


class FormTests(TestCase):

    def setUp(self):
        self.user = UserFactory()

    def test_form_task_should_be_valid_and_save_record(self):
        form_data = {"title": "next_title", "text": "more text", "status": "todo", "author": "1"}
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

        form.save()
        self.assertEqual(Task.objects.count(), 1)
