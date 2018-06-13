from django import forms
from django.forms import ModelForm

from .models import Task


class TodoForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "text", "status"]
        widgets = {'status': forms.HiddenInput()}

    def save(self, commit=True):
        instance = super(TodoForm, self).save(False)
        instance.status = "todo"
        if commit:
            instance.save()
        return instance


class InprogressForm(TodoForm):

    def save(self, commit=True):
        instance = super(InprogressForm, self).save(False)
        instance.status = "in progress"
        if commit:
            instance.save()
        return instance


class DoneForm(TodoForm):

    def save(self, commit=True):
        instance = super(DoneForm, self).save(False)
        instance.status = "done"
        if commit:
            instance.save()
        return instance
