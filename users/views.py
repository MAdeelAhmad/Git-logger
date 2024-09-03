from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import subprocess

from .models import TechStack
from .forms import RegisterForm, LoginForm, UpdateUserForm, UpdateProfileForm, TechStackForm

def home(request):
    return render(request, 'users/home.html')

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to='/')

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})

class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            self.request.session.set_expiry(0)
            self.request.session.modified = True

        return super(CustomLoginView, self).form_valid(form)

class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('users-home')

@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='users-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})

@login_required
def select_tech_stack(request):
    if request.method == 'POST':
        form = TechStackForm(request.POST)
        if form.is_valid():
            language = form.cleaned_data['language']
            user=request.user
            TechStack.objects.create(user=user, language=language)
            github_auth = user.social_auth.get(provider='github')
            token = github_auth.extra_data['access_token']
            try:
                first_name = user.first_name if user.first_name else user
                result = subprocess.run(['users/tmp/github_scripts.sh', str(user), str(first_name), str(user.email), str(token), str(language)], capture_output=True, text=True, check=True)

                script_output = result.stdout
                script_error = result.stderr

                print(f"Script output: {script_output}")
                if script_error:
                    print(f"Script error: {script_error}")

            except subprocess.CalledProcessError as e:
                return JsonResponse({"error": "Failed to run the script", "details": str(e)}, status=500)

            messages.success(request, 'Tech stack added successfully.')
            return redirect(to='select_tech_stack')
    else:
        form = TechStackForm()
    
    return render(request, 'select_tech_stack.html', {'form': form})
