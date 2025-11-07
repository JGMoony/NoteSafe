from django.urls import path
from . import views
from .views import ProfileDetailView, ProfileUpdateView, ProfileDeleteView

app_name = 'users'

urlpatterns = [
    path('perfil/', views.ProfileDetailView.as_view(), name='profile_detail'),
    path('perfil/editar/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/delete/<int:pk>/', views.ProfileDeleteView.as_view(), name='profile_delete'),
]