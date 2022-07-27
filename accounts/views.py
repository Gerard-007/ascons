import json

from django.conf import settings
from django.contrib import messages, auth
from django.contrib.auth import logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import generic
from django.views.generic.base import View
from validate_email import validate_email

from accounts.forms import UserChangeForm
from accounts.models import User
from accounts.token import account_activation_token


class EmailValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Wrong email address...'}, status=400)
        if User.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'Sorry email already in use...'}, status=409)
        return JsonResponse({'email-valid': True})


class UsernameValidationView(View):

    def post(self, request):
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'Username should contain alphanumeric characters...'}, status=400)
        if User.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'Sorry username already in use...'}, status=409)
        return JsonResponse({'username-valid': True})


class RegistrationView(View):

    def get(self, request):
        return render(request, 'accounts/signup.html')

    def post(self, request):
        # get user data
        username = request.POST['username']
        email = request.POST['email']
        # business_name = request.POST['business_name']
        password = request.POST['password']

        context = {
            'fieldValues': request.POST
        }
        # validate data
        if (
                not User.objects.filter(username=username).exists()
                and not User.objects.filter(email=email).exists()
        ):
            if len(password) < 6:
                messages.error(request, "password is too short")
                return render(request, 'accounts/signup.html', context)
            # else create user account but dont activate the user
            user = User.objects.create_user(username=username, email=email)
            user.set_password(password)
            user.is_active = True  # TODO change back to False when email is working...
            user.save()
            # # -> getting Domain we are on...
            # domain = get_current_site(request).domain
            # # -> Encode uid
            # uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            # # -> Token
            # token = account_activation_token.make_token(user)
            # message = "confirm your registration"
            # # -> Relative Url to verification...
            # link = reverse('accounts:activate', kwargs={'uidb64': uidb64, 'token': token})
            # # ========== Send activation email to user ============
            # email_template = render_to_string('accounts/account_activation_email.html',
            #                                   {'user': user.username, 'domain': domain, 'link': link,
            #                                    'message': message})
            # send_mail = EmailMessage(
            #     'Activate your segsbytes account',
            #     email_template,
            #     settings.SUPPORT_EMAIL,
            #     [email],
            # )
            # send_mail.fail_silently = False
            # send_mail.send()

            # ============== send success message to user =============
            # messages.success(request, "Account Created!, Check your email to activate your account")
            # -> Login user
            auth.login(request, auth.authenticate(
                email=email,
                password=password,
            ))
            messages.success(request,
                             'Account created and login successful!, please update you credentials')
            return redirect("accounts:profile_update", slug=user.slug)
            # messages.success(request,
            #                  'Account created successfully!, You can now login with your registered credentials')
            # return render(request, 'accounts/signup.html', context)
        return render(request, 'accounts/signup.html')


class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=id)

            # -> check if user have clicked on authentication token
            if not account_activation_token.check_token(user, token):
                return redirect("accounts:login" + "?message=" + "User already activated")

            # -> Activate user if activation token is clicked
            if user.is_active:
                return redirect("accounts:login")
            user.is_active = True
            user.save()

            # -> Display success message after activation
            messages.success(request, "Account activated successfully")

            # -> Login user
            auth.login(request, auth.authenticate(
                email=user.email,
                password=user.password, )
                       )
            return redirect("accounts:profile_update", slug=user.slug)
            # return redirect("accounts:profile_update", kwargs={'slug': user.slug})

        except Exception as ex:
            messages.error(request, "Email not delivered due to your Network, try again")
            return redirect("accounts:login")


class LoginView(View):
    def get(self, request):
        return render(request, 'accounts/login.html')

    def post(self, request):
        email = request.POST["email"]
        password = request.POST['password']

        if email and password:
            user = auth.authenticate(email=email, password=password)

            if user:

                if user.is_active:
                    auth.login(request, user)
                    messages.success(request, f"Welcome, {user.username} login was successful...")
                    return redirect('home')
                messages.error(request, 'Account is not active,please check your email')
                return render(request, 'accounts/login.html')

            messages.error(request, 'Invalid credentials,try again')
            return render(request, 'accounts/login.html')

        messages.error(request, 'Please fill all fields')
        return render(request, 'accounts/login.html')


class LogoutView(generic.RedirectView):
    url = reverse_lazy("home")

    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, "You have successfully Logged out.")
        return super(LogoutView, self).get(request, *args, **kwargs)


class PasswordResetView(View):
    def get(self, request):
        return render(request, "accounts/reset-password.html")

    def post(self, request):
        email = request.POST['email']

        context = {
            'values': request.POST
        }

        if not validate_email(email):
            messages.error(request, "please supply a valid email")
            return render(request, 'accounts/reset-password.html', context)

        # -> getting Domain we are on...
        current_site = get_current_site(request).domain
        user = User.objects.filter(email=email)

        if user.exists():
            uid = urlsafe_base64_encode(force_bytes(user[0].pk))
            token = PasswordResetTokenGenerator().make_token(user[0])
            link = reverse('accounts:reset-user-password', kwargs={'uidb64': uid, 'token': token})
            message = "reset your password"
            # ========== Send activation email to user ============
            email_template = render_to_string('accounts/account_activation_email.html',
                                              {'user': user[0].username, 'domain': current_site, 'link': link,
                                               'message': message})
            send_mail = EmailMessage(
                'Reset your Zebeja account password',
                email_template,
                settings.SUPPORT_EMAIL,
                [email],
            )
            send_mail.fail_silently = False
            send_mail.send()
            messages.success(request, "We have sent a password reset link to your email")
            return render(request, 'accounts/reset-password.html', context)
        messages.info(request, "Email does not exist")
        return render(request, 'accounts/reset-password.html', context)


class CompletePasswordResetView(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)

            if not PasswordResetTokenGenerator().check_token(user):
                messages.info(request, "Password link is invalid, please request for a new password")
                return render(request, 'accounts/reset-password.html', context)
        except Exception as ex:
            return render(request, 'accounts/set-new-password.html', context)

    def post(self, request, uidb64, token):
        context = {
            'uidb64': uidb64,
            'token': token
        }
        password = request.POST['password']
        password2 = request.POST['password2']

        if password != password2:
            messages.error(request, "Password do not match.")
            return render(request, 'accounts/set-new-password.html', context)
        if len(password) < 6:
            messages.error(request, "Password is too short.")
            return render(request, 'accounts/set-new-password.html', context)

        try:
            user_id = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=user_id)
            user.set_password(password)
            user.save()
            messages.success(request, "Password reset successfully, you can login with your new password")
            return redirect('accounts:login')
        except Exception as ex:
            messages.info(request, "Something was wrong...")
            return render(request, 'accounts/set-new-password.html', context)


class UserProfileView(LoginRequiredMixin, generic.DetailView):
    template_name = "accounts/profile.html"
    model = User

    def get_object(self, *args, **kwargs):
        user_obj = self.request.user
        print(user_obj)
        return user_obj


class UpdateUserProfileView(LoginRequiredMixin, generic.DetailView, generic.UpdateView):
    template_name = "accounts/update_profile.html"
    model = User
    form_class = UserChangeForm

    def get_object(self, queryset=None, *args, **kwargs):
        return self.request.user

    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'slug': self.request.user.slug})
