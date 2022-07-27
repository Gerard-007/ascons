from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from accounts import views

urlpatterns = [
    path('signup/', views.RegistrationView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('profile/<slug:slug>', views.UserProfileView.as_view(), name='profile'),
    path('update/<slug:slug>/', views.UpdateUserProfileView.as_view(), name='profile_update'),
    path('set-new-password/<uidb64>/<token>/', views.CompletePasswordResetView.as_view(), name='reset-user-password'),
    path('reset/', views.PasswordResetView.as_view(), name='reset-password'),
    path('validate-username/', csrf_exempt(views.UsernameValidationView.as_view()), name='validate-username'),
    path('validate-email/', csrf_exempt(views.EmailValidationView.as_view()), name='validate-email'),
    path('activate/<uidb64>/<token>/', views.VerificationView.as_view(), name='activate'),

    # path('accounts/signup/teacher/', views.TeacherSignUpView.as_view(), name='teacher_signup'),
]
