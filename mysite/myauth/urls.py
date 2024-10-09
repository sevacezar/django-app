from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, reverse_lazy

from .views import (
    login_view,
    set_cookie_view,
    get_cookie_view,
    set_session_view,
    get_session_view,
    logout_view,
    MyLogoutPage,
    AboutMe,
    RegisterView,
    FooBarView,
    UsersListView,
    UserDetailView,
    HelloView,
    )


app_name = 'myauth'

urlpatterns = [
    # path('login/', login_view, name='login'),
    path('', UsersListView.as_view(), name='users_list'),
    path('<int:pk>/', UserDetailView.as_view(), name='user_details'),
    path('about-me/', AboutMe.as_view(), name='about-me'),
    path(
        'login/',
        LoginView.as_view(
            template_name='myauth/login.html',
            redirect_authenticated_user=True,            
            ),
            name='login',
    ),
    path('cookie/get/', get_cookie_view, name='cookie-get'),
    path('cookie/set/', set_cookie_view, name='cookie-set'),
    path('session/get/', get_session_view, name='session-get'),
    path('session/set/', set_session_view, name='session-set'),
    path('logout/', MyLogoutPage.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('foobar/', FooBarView.as_view(), name='foo-bar'),

    path('hello/', HelloView.as_view(), name='hello'),
]
