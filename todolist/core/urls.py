from django.urls import path

from .views import SignUpView, LoginView, RetrieveUpdateView, PasswordUpdateView

urlpatterns = [
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('profile', RetrieveUpdateView.as_view()),
    path('update_password', PasswordUpdateView.as_view())
]
