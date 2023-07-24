from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from . import views


app_name = "main"   

urlpatterns = [
    path("", csrf_exempt(views.RegistrationView.as_view()), name="homepage"),
    path("pass", csrf_exempt(views.PasswordView.as_view()), name="home"),
    path("validate-username", csrf_exempt(views.UsernameValidationView.as_view()), name="validate-username"),
    path("validate-lastname", csrf_exempt(views.LastnameValidationView.as_view()), name="validate-lastname"),
    path("validate-password", csrf_exempt(views.PasswordValidation.as_view()), name="validate-password"),
]