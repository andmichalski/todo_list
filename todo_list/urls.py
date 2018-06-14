"""todo_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from todo.views import TaskListView, TaskDetailView, TaskFormView, DeleteTaskView, UpdateStatusView, SignupUserView
from django.urls import reverse_lazy
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', TaskListView.as_view(), name="tasklist"),
    url(r'^task/(?P<pk>\d+)/$', TaskDetailView.as_view(), name="taskdetail"),
    url(r'^new_task/(?P<string>[\w\-]+)/$', TaskFormView.as_view(), name="taskform"),
    url(r'^delete/(?P<pk>\d+)/$', DeleteTaskView.as_view(), name="deletetask"),
    url(r'^update/(?P<pk>\d+)/$', UpdateStatusView.as_view(), name="updatestatus"),
    url(r'^login/$', LoginView.as_view(), name="loginview"),
    url(r'^logout/$', LogoutView.as_view(), name="logoutview"),
    url(r'^signup/$', SignupUserView.as_view(), name="signupview"),

]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns = [
                      url(r'^__debug__/', include(debug_toolbar.urls)),
                  ] + urlpatterns
