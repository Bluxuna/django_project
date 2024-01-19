from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from users.forms import CustomUserCreateForm

class SignUpView(CreateView):
    form_class = CustomUserCreateForm
    template_name = 'registration/user_create_form.html'
    success_url = reverse_lazy('users:login')
