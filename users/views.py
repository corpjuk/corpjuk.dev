from django.contrib.auth import authenticate, login, logout
# from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect
from django.urls import reverse

from .forms import RegisterForm, LogInForm



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

def login_view(request):
    error = False
    # if request.user.is_authenticated:
    #     return redirect('home')
    if request.method == "POST":
        form = LogInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                # return render(request, "accounts/login.html", {})
                return redirect('home')
            else:
                error = True
    else:
        form = LogInForm()

    return render(request, 'accounts/login.html', {'form': form, 'error': error})

# def login_view(request):

#     # future -> ?next=/articles/create or handle redirects in settings    
#     if request.method == "POST":
#         form = AuthenticationForm(request, data=request.POST)
#         if form.is_valid():
#             user = form.get_user()
#             login(request, user)
#             return redirect('/')
#     else:
#         form = AuthenticationForm(request)
#     context = {"form": form }
#     return render(request, "accounts/login.html", context)

# def logout_view(request):
#     logout(request)
#     return redirect(reverse('users:login'))

def logout_view(request):
    if request.method == "POST":
        logout(request)
        return redirect('home')
    return render(request, "accounts/logout.html", {})
