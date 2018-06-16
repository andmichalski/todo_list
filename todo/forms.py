from django import forms
from django.forms import ModelForm

from .models import Task


class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ["title", "text", "status", "author"]
        widgets = {'status': forms.HiddenInput(),
                   'author': forms.HiddenInput()}

    def save(self, new_status, commit=True):
        instance = super(TaskForm, self).save(False)
        instance.status = new_status
        if commit:
            instance.save()
        return instance
