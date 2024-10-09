from random import random

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.urls import reverse, reverse_lazy
from django.contrib.auth.views import LogoutView
from django.views.generic import TemplateView, CreateView, ListView, DetailView
from django.views import View
from django.views.decorators.cache import cache_page
from django.utils.translation import gettext_lazy as _, ngettext

from .forms import AvatarUpdateForm
from .models import Profile


class AboutMe(TemplateView):
    template_name = 'myauth/about-me.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем информацию о пользователе и его профиле в контекст
        context['user'] = self.request.user
        context['form'] = AvatarUpdateForm(instance=self.request.user.profile)
        return context

    def post(self, request, *args, **kwargs):
        form = AvatarUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('myauth:about-me')
        # Если форма не валидна, повторно рендерим страницу с формой и ошибками
        return self.render_to_response(self.get_context_data(form=form))


class UsersListView(ListView):
    queryset = User.objects.select_related('profile')
    template_name = 'myauth/user_list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    queryset = User.objects.select_related('profile')
    template_name = 'myauth/user_detail.html'
    context_object_name = 'user'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем информацию о пользователе и его профиле в контекст
        # context['user'] = self.request.user
        context['form'] = AvatarUpdateForm(instance=self.request.user.profile)
        context['can_edit'] = (self.request.user == self.get_object() or self.request.user.is_staff)
        return context

    def post(self, request, *args, **kwargs):
        form = AvatarUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if form.is_valid():
            form.save()
            return redirect('myauth:about-me')
        # Если форма не валидна, повторно рендерим страницу с формой и ошибками
        return self.render_to_response(self.get_context_data(form=form))



class RegisterView(CreateView):
    # Просто создает пользователя. Не аутентифицирует его
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    # Доработаем
    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')

        user = authenticate(self.request, username=username, password=password)
        login(self.request, user=user)
        return response

def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('/admin/')
        
        return render(request, 'myauth/login.html')
    
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)  # Return user (if its ok with auth) or None (if not)

    if user:
        login(request, user)
        return redirect('/admin/')
    return render(request, 'myauth/login.html', {'error': 'Invalid login credentials'})


class MyLogoutPage(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        logout(request)
        return redirect('myauth:login')

@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request: HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie Set')
    response.set_cookie('some_cookie', 'some_value', max_age=3600)
    return response

@cache_page(60 * 2)
def get_cookie_view(request: HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('some_cookie', 'default_value')

    return HttpResponse(f'Cookie value: {value!r} + {random()}')  # random for cache testing

@permission_required('myauth.view_profile', raise_exception=True)
def set_session_view(request: HttpRequest) -> HttpResponse:
    request.session['info'] = 'some_info'
    return HttpResponse('Session set!')

@login_required
def get_session_view(request: HttpRequest) -> HttpResponse:
    value = request.session.get('info', 'default_info')
    return HttpResponse(f'Session value {value!r}')

def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request=request)
    return redirect(reverse('myauth:login'))  # reverse work only in view functions!

class FooBarView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        return JsonResponse({'foo': 'bar', 'spam': 'eggs'})
    


class HelloView(View):
    welcome_message = _('welcome hello world')
    def get(self, request: HttpRequest) -> HttpResponse:
        items_str = request.GET.get('items') or 0
        items = int(items_str)
        products_line = ngettext(
            'one product',
            '{count} products',
            items,
        )
        products_line = products_line.format(count=items)
        return HttpResponse(f'<h1>{self.welcome_message}</h1>'
                            f'\n<h2>{products_line}</h2>')
    