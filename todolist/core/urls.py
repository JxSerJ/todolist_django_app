from django.urls import path

from .views import SignUpView, LoginView, RetrieveUpdateView

urlpatterns = [
    path('signup', SignUpView.as_view()),
    path('login', LoginView.as_view()),
    path('profile', RetrieveUpdateView.as_view()),
]
