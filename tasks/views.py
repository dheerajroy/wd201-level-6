from django.shortcuts import render, redirect
from numpy import delete
from .models import Task
from django.views.generic import (ListView, CreateView, DetailView, UpdateView, DeleteView)
from .forms import CreateUpdateTaskForm

class AllTasksView(ListView):
    """Displays all tasks"""
    template_name = 'all_tasks.html'
    paginate_by = 10
    context_object_name = 'tasks'

    def get_queryset(self):
        self.status = self.request.GET.get('status')
        if self.status == 'pending':
            return Task.objects.filter(user=self.request.user, completed=False, deleted=False).order_by('priority')
        elif self.status == 'completed':
            return Task.objects.filter(user=self.request.user, completed=True, deleted=False).order_by('priority')
        elif self.status == 'all' or self.status == None:
            self.status = 'all'
            return Task.objects.filter(user=self.request.user, deleted=False).order_by('priority')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        pending_tasks = len(Task.objects.filter(user=self.request.user, completed=False, deleted=False).order_by('priority'))
        completed_tasks = len(Task.objects.filter(user=self.request.user, completed=True, deleted=False))
        context['completed_ratio'] = f'{completed_tasks} of {pending_tasks+completed_tasks} tasks completed'
        context['request_type'] = self.status
        return context

class DetailTaskView(DetailView):
    model = Task
    template_name = 'task.html'

def priority_updater(priority, user):
    tasks = Task.objects.filter(user=user, priority__gte=priority, deleted=False)
    prev_priority = -1
    for task in tasks:
        if prev_priority > 0 and prev_priority != task.priority:
            break
        task.priority += 1
        task.save()

class CreateTaskView(CreateView):
    form_class = CreateUpdateTaskForm
    template_name = 'create_update_task.html'
    success_url = '/'
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        priority_updater(form.instance.priority, self.request.user)
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Create'
        return context

class UpdateTaskView(UpdateView):
    form_class = CreateUpdateTaskForm
    model = Task
    template_name = 'create_update_task.html'
    success_url = '/'

    def form_valid(self, form):
        priority_updater(form.instance.priority, self.request.user)
        # form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['type'] = 'Update'
        return context

class DeleteTaskView(DeleteView):
    model = Task
    template_name = 'delete.html'
    success_url = '/'
