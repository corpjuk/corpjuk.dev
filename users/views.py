from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse
from django.template.context_processors import csrf

from crispy_forms.utils import render_crispy_form
from .forms import RegisterForm, LogInForm, ProfileForm

# Create your views here.


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

# def register_view(request):
#     form = UserCreationForm(request.POST or None)
#     if form.is_valid():
#         user_obj = form.save()
#         return redirect('/login')
#     context = {"form": form}
#     return render(request, "accounts/register.html", context)

# def login_view(request):
#     error = False
#     # if request.user.is_authenticated:
#     #     return redirect('home')
#     if request.method == "POST":
#         form = LogInForm(request.POST)
#         if form.is_valid():
#             username = form.cleaned_data["username"]
#             password = form.cleaned_data["password"]
#             user = authenticate(username=username, password=password)
#             if user:
#                 login(request, user)
#                 # return render(request, "accounts/login.html", {})
#                 return redirect('home')
#             else:
#                 error = True
#     else:
#         form = LogInForm()

#     return render(request,
#                   'accounts/login.html',
#                   {'form': form, 'error': error})


def login_view(request):
    # future -> ?next=/articles/create or handle redirects in settings
    context = {"form": AuthenticationForm()}
    template_name = "accounts/login.html"
    if request.method == "GET":
        form = AuthenticationForm()
        template_name = "accounts/partials/loginbutton.html"
        return render(request, template_name, context)
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            template_name = "accounts/partials/successfullogin.html"
            user = form.get_user()
            login(request, user)
            return render(request, template_name, {})
    else:
        template_name = "accounts/login.html"
        form = AuthenticationForm(request)
    return render(request, template_name, context)
    # return render(request, "accounts/login.html", context)


def logout_view(request):
    template_name = "accounts/partials/loginbutton.html"
    if request.method == "POST":
        template_name = "accounts/partials/successfullogout.html"
        logout(request)
        return render(request, template_name, {})
        # return redirect('home')
    return render(request, template_name, {})


def profile_view(request):

    if request.method == 'GET':
        context = {'form': ProfileForm()}
        # context = {'form': ProfileForm()}
        # context = {'form': LogInForm()}
        return render(request, "accounts/profile.html", context)

    elif request.method == 'POST':
        # form = ProfileForm(request.POST)
        form = LogInForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return HttpResponse(redirect('/login'))
        ctx = {}
        ctx.update(csrf(request))
        form_html = render_crispy_form(form, context=ctx)
        return HttpResponse(form_html)
        # I need to override the default save method for security?
        # https://www.youtube.com/watch?v=ZxvhAKT0Wwo&ab_channel=BugBytes
        
