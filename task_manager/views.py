from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models import ProtectedError
from .models import Status



def index(request):
    return render(request, 'task_manager/index.html')



class UserListView(ListView):
    model = User
    template_name = 'task_manager/user_list.html'
    context_object_name = 'object_list'


class UserCreateView(CreateView):
    model = User
    template_name = 'task_manager/user_form.html'
    fields = ['username', 'password', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        messages.success(self.request, 'User registered successfully')
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = User
    template_name = 'task_manager/user_form.html'
    fields = ['username', 'first_name', 'last_name', 'email']
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.get_object() == self.request.user

    def form_valid(self, form):
        messages.success(self.request, 'User updated successfully')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'task_manager/user_confirm_delete.html'
    success_url = reverse_lazy('user_list')

    def test_func(self):
        return self.get_object() == self.request.user

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'User deleted successfully')
        return super().delete(request, *args, **kwargs)


class UserLoginView(LoginView):
    template_name = 'task_manager/login.html'

    def get_success_url(self):
        messages.success(self.request, 'You are logged in successfully')
        return reverse_lazy('home')


class UserLogoutView(LogoutView):
    next_page = reverse_lazy('login')

    def dispatch(self, request, *args, **kwargs):
        messages.success(self.request, 'You have been logged out')
        return super().dispatch(request, *args, **kwargs)


class StatusListView(LoginRequiredMixin, ListView):
    model = Status
    template_name = 'task_manager/status_list.html'
    context_object_name = 'statuses'


class StatusCreateView(LoginRequiredMixin, CreateView):
    model = Status
    template_name = 'task_manager/status_form.html'
    fields = ['name']
    success_url = reverse_lazy('status_list')

    def form_valid(self, form):
        messages.success(self.request, 'Status created successfully')
        return super().form_valid(form)


class StatusUpdateView(LoginRequiredMixin, UpdateView):
    model = Status
    template_name = 'task_manager/status_form.html'
    fields = ['name']
    success_url = reverse_lazy('status_list')

    def form_valid(self, form):
        messages.success(self.request, 'Status updated successfully')
        return super().form_valid(form)


class StatusDeleteView(LoginRequiredMixin, DeleteView):
    model = Status
    template_name = 'task_manager/status_confirm_delete.html'
    success_url = reverse_lazy('status_list')

    def delete(self, request, *args, **kwargs):
        try:
            messages.success(self.request, 'Status deleted successfully')
            return super().delete(request, *args, **kwargs)
        except ProtectedError:
            messages.error(self.request, 'Cannot delete status because it is in use')
            return redirect('status_list')