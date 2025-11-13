from django.urls import path
from . import views
from .views import ProfileDetailView, ProfileUpdateView, ProfileDeleteView, AdminDashboardView, admin_home_view

app_name = 'users'

urlpatterns = [
    path('perfil/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('perfil/editar/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/delete/<int:pk>/', views.ProfileDeleteView.as_view(), name='profile_delete'),
    path('admin/dashboard/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin/home/', admin_home_view, name='admin_home'),
]