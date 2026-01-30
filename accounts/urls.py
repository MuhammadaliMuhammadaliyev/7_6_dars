from django.urls import path
from .views import SignUpView, LoginView, ProfileView, ProfileUpdateView, \
    LogoutView, ChangePasswordView, ResetCodeView

urlpatterns = [
    path('sign-up/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('profile/', ProfileView.as_view()),
    path('profile-update/', ProfileUpdateView.as_view()),
    path("change-password/", ChangePasswordView.as_view()),
    path("auth/reset/verify-code/", ResetCodeView.as_view()),
]
