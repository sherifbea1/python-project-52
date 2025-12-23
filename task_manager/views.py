from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    DetailView,
)
from django.db.models import ProtectedError

from .models import Status, Task, Label


def index(request):
    return render(request, 'task_manager/index.html')


class UserListView(ListView):
    model = User
    template_name = 'task_manager/user_list.html'
    context_object_name = 'object_list'
    ordering = ['id']



class UserCreateView(CreateView):
    model = User
    form_class = UserCreationForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'User registered successfully.')
        return response


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'task_manager/user_form.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.get_object() == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'User updated successfully.')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'task_manager/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.get_object() == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You cannot delete another user.")
        return redirect('user_list')

    def delete(self, request, *args, **kwargs):
        try:
            messages.success(self.request, 'User deleted successfully.')
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(
                self.request,
                'Cannot delete user because they are assigned to tasks.'
            )
            return redirect('user_list')


class UserLoginView(LoginView):
    template_name = 'task_manager/login.html'

    def get_success_url(self):
        messages.success(self.request, 'Вы залогинены')
        return reverse_lazy('home')



class UserLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, 'Вы разлогинены')
        return redirect('home')


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'task_manager/status_list.html'
    context_object_name = 'statuses'
    ordering = ['id']


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'task_manager/status_form.html'
    fields = ['name']
    success_url = reverse_lazy('status_list')

    def form_valid(self, form):
        messages.success(self.request, 'Status created successfully.')
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'task_manager/status_form.html'
    fields = ['name']
    success_url = reverse_lazy('status_list')

    def form_valid(self, form):
        messages.success(self.request, 'Status updated successfully.')
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'task_manager/status_confirm_delete.html'
    success_url = reverse_lazy('status_list')

    def delete(self, request, *args, **kwargs):
        try:
            response = super().delete(request, *args, **kwargs)
            messages.success(request, 'Status deleted successfully.')
            return response
        except ProtectedError:
            messages.error(
                request,
                'Cannot delete status because it is in use.'
            )
            return redirect('status_list')

class TaskListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_manager/task_list.html'
    context_object_name = 'tasks'
    ordering = ['-created_at']

    def get_queryset(self):
        queryset = super().get_queryset()

        status_id = self.request.GET.get("status")
        executor_id = self.request.GET.get("executor")
        label_id = self.request.GET.get("labels")
        only_my = self.request.GET.get("only_my")

        if status_id:
            queryset = queryset.filter(status_id=status_id)
        if executor_id:
            queryset = queryset.filter(executor_id=executor_id)
        if label_id:
            queryset = queryset.filter(labels__id=label_id)
        if only_my:
            queryset = queryset.filter(author=self.request.user)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["statuses"] = Status.objects.all()
        context["users"] = User.objects.all()
        context["labels"] = Label.objects.all()
        return context


class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'task_manager/task_detail.html'
    context_object_name = 'task'


class TaskCreateView(LoginRequiredMixin, CreateView):
    model = Task
    template_name = 'task_manager/task_form.html'
    fields = ['name', 'description', 'status', 'executor', 'labels']
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, 'Task created successfully.')
        return super().form_valid(form)


class TaskUpdateView(LoginRequiredMixin, UpdateView):
    model = Task
    template_name = 'task_manager/task_form.html'
    fields = ['name', 'description', 'status', 'executor', 'labels']
    success_url = reverse_lazy('task_list')

    def form_valid(self, form):
        messages.success(self.request, 'Task updated successfully.')
        return super().form_valid(form)


class TaskDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Task
    template_name = 'task_manager/task_confirm_delete.html'
    success_url = reverse_lazy('task_list')

    def test_func(self):
        return self.get_object().author == self.request.user

    def handle_no_permission(self):
        messages.error(
            self.request,
            "You cannot delete someone else's task."
        )
        return redirect('task_list')

    def delete(self, request, *args, **kwargs):
        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Task deleted successfully.')
        return response



class LabelListView(LoginRequiredMixin, ListView):
    model = Label
    template_name = 'task_manager/label_list.html'
    context_object_name = 'labels'
    ordering = ['id']


class LabelCreateView(LoginRequiredMixin, CreateView):
    model = Label
    template_name = 'task_manager/label_form.html'
    fields = ['name']
    success_url = reverse_lazy('label_list')

    def form_valid(self, form):
        messages.success(self.request, 'Label created successfully.')
        return super().form_valid(form)


class LabelUpdateView(LoginRequiredMixin, UpdateView):
    model = Label
    template_name = 'task_manager/label_form.html'
    fields = ['name']
    success_url = reverse_lazy('label_list')

    def form_valid(self, form):
        messages.success(self.request, 'Label updated successfully.')
        return super().form_valid(form)


class LabelDeleteView(LoginRequiredMixin, DeleteView):
    model = Label
    template_name = 'task_manager/label_confirm_delete.html'
    success_url = reverse_lazy('label_list')

    def delete(self, request, *args, **kwargs):
        label = self.get_object()

        if label.tasks.exists():
            messages.error(
                request,
                'Cannot delete label because it is associated with tasks.'
            )
            return redirect('label_list')

        response = super().delete(request, *args, **kwargs)
        messages.success(request, 'Label deleted successfully.')
        return response
