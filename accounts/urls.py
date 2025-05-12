from django.urls import path
from .views import (
    register, profile, update_profile, logout_view, login_view,
    RegisterView, UserProfileView,
    UserUpdateView, UserListView, LogoutView
)

app_name = 'accounts'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/', register, name='register'),
    path('profile/', profile, name='profile'),
    path('profile/update/', update_profile, name='update'),
    path('logout/', logout_view, name='logout'),
    path('api/register/', RegisterView.as_view(), name='api-register'),
    path('api/profile/', UserProfileView.as_view(), name='api-profile'),
    path('api/update/', UserUpdateView.as_view(), name='api-update'),
    path('api/users/', UserListView.as_view(), name='api-user-list'),
    path('api/logout/', LogoutView.as_view(), name='api-logout'),
] 