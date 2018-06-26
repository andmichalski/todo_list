from django import forms
from django.forms import ModelForm

from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "text", "status", "author"]
        widgets = {'status': forms.HiddenInput(),
                   'author': forms.HiddenInput()}


class TaskUpdateForm(ModelForm):
    class Meta:
        model = Task
        fields = ["status"]
