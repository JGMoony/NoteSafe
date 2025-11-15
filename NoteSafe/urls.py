from django.contrib import admin
from django.urls import path, include
from users.views import AdminDashboardView, custom_redirect_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('notes.urls')),
     # Tu vista al entrar a /accounts/


    # Allauth sigue funcionando para login, signup, confirm-email, etc
    path('accounts/', include('allauth.urls')),
    path('users/', include('users.urls')),
    path('admin/', AdminDashboardView.as_view(), name='admin_dashboard'),
    path('redirect-home', custom_redirect_view, name='redirect_home'),
]
