from django.urls import path, include
from django.conf.urls import *
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(redirect_authenticated_user=True)),
    path('editorlogin/', auth_views.LoginView.as_view(
        template_name="registration/EditorLogin.html",
        redirect_authenticated_user=True,
        extra_context={
            'next': 'editor_home'
        }
    )),
    path('logout/', auth_views.LogoutView.as_view()),
    path('password_change/', auth_views.PasswordChangeView.as_view()),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view()),
    path('password_reset/', auth_views.PasswordResetView.as_view()),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view()),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view()),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view()),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.Signup.as_view(success_url="/"), name='signup'),
]
