from django.contrib.auth.views import LoginView
from django.views.generic import CreateView

from .forms import AuthenticationForm, UserCreationForm


class UserLoginView(LoginView):
    form_class = AuthenticationForm
    template_name = "login.html"


class UserSignupView(CreateView):
    form_class = UserCreationForm
    template_name = "signup.html"
    success_url = "/accounts/login/"