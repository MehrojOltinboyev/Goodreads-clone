from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from users.models import CustomUser
from django.shortcuts import render, redirect
from django.views import View
from users.forms import CustomUserCreationForm, UserUpdateForm # ✅ to‘g‘ri forma

class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('users:login')  # login sahifaga o'tkazish
        return render(request, 'users/register.html', {'form': form})

class LoginView(View):
    def get(self, request):
        login_form = AuthenticationForm()
        return render(request, 'users/login.html', {"login_form":login_form})


    def post(self, request):
        login_form = AuthenticationForm(data=request.POST)

        if login_form.is_valid():
            user = login_form.get_user()
            login(request, user)
            messages.success(request, "You have successfully logged in")
            return redirect("books:list")
        else:
            return render(request, 'users/login.html', {"login_form": login_form})





class ProfileView(LoginRequiredMixin,View):
    def get(self, request):
        context = {"user": request.user}
        return render(request, "users/profile.html", context=context)


class LogoutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.info(request, "You have successfully logged out.")
        return redirect("landing_page")


class ProfileupdateView(LoginRequiredMixin, View):
    def get(self, request):
        user_update_form = UserUpdateForm(instance=request.user)

        return render(request=request, template_name="users/profile_edit.html",context={"form":user_update_form})

    def post(self, request):
        user_update_form = UserUpdateForm(instance=request.user,data=request.POST,files=request.FILES)
        if user_update_form.is_valid():
            user_update_form.save()
            messages.success(request, "You have successfully updated your profile.")

            return redirect("users:profile")

        return render(request, "users/profile_edit.html", {"form":user_update_form})




























# from users.models import CustomUser
# from django.shortcuts import render, redirect
# from django.views import View
# from users.forms import UserCreateForm
#
# # Create your views here.
#
# class RegisterView(View):
#     def get(self, request):
#         create_form = UserCreateForm()
#         context = {
#             "form":create_form
#         }
#         return render(request=request, template_name='users/register.html', context=context)
#
#     def post(self, request):
#         create_form = UserCreateForm(data=request.POST)
#         if create_form.is_valid():
#             create_form.save()
#             #create user account
#             return redirect('users:login')
#         else:
#             context = {
#                 "form": create_form
#             }
#             return render(request=request, template_name="users/register.html",context=context)
#
# class LoginView(View):
#     def get(self, request):
#         return render(request=request, template_name='users/login.html')