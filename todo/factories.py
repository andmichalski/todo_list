import factory

from .models import Task
from django.contrib.auth.models import User

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
