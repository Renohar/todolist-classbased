from typing import ContextManager
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView,UpdateView,DeleteView,FormView
from base.models import *
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


# Create your views here.
class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields ="__all__"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('list')

class TaskList(LoginRequiredMixin,ListView):
    model = Task
    template_name = 'base/list.html'
    context_object_name = 'tasks'

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        # search_input = self.request.GET.get('searcharea') or ''
        # if search_input:
        #     context['tasks'] =context['tasks'].filter(title__startswith=search_input)
        # context['search_input'] = search_input
        return context

class TaskDetail(LoginRequiredMixin,DetailView):
    model = Task
    template_name = 'base/detail.html'
    context_object_name = 'tasks'


class TaskCreate(LoginRequiredMixin,CreateView):
    model = Task
    fields = ['title','description','complete']
    template_name = 'base/create.html'
    context_object_name = 'tasks'
    success_url = reverse_lazy('list')

    def form_valid(self,form):
        form.instance.user = self.request.user
        return super(TaskCreate,self).form_valid(form)

class TaskUpdate(LoginRequiredMixin,UpdateView):
    model = Task
    fields ="__all__"
    template_name ='base/update.html'
    context_object_name = 'tasks'
    success_url = reverse_lazy('list')

class TaskDelete(LoginRequiredMixin,DeleteView):
    model = Task
    context_object_name ='tasks'
    template_name ='base/delete.html'
    success_url = reverse_lazy('list')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('list')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage,self).form_valid(form)
    
    def get(self,*args,**kwargs):
        if self.request.user.is_authenticated:
            return redirect('list')
        return super(RegisterPage,self).get(*args,**kwargs)