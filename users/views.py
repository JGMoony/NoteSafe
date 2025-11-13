from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import UpdateView, DetailView, DeleteView, TemplateView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.db.models import Count
from notes.models import Note, Tag, AuditLog
from .forms import ProfileUpdateForm
from users.models import User


User = get_user_model()

class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = ProfileUpdateForm
    template_name = 'users/profile_edit.html'
    
    success_url = reverse_lazy('notes:note_list') 

    def get_object(self, queryset=None):
        return self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context
    
    
class ProfileDetailView(DetailView, LoginRequiredMixin):
    model = User
    template_name = 'users/profile_detail.html'

    def get_object(self, queryset=None):
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        total_notes = Note.objects.filter(user=user).count()
        
        most_used_tags = Tag.objects.filter(user=user) \
            .annotate(note_count=Count('note')) \
            .order_by('-note_count')[:3]
            
        context['stats'] = {
            'total_notes': total_notes,
            'most_used_tags': most_used_tags,
        }
        
        return context


class AccountDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'core/profile_confirm_delete.html'
    success_url = reverse_lazy('account_login') 
    
    def get_object(self, queryset=None):
        return self.request.user
    
    
class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/profile_confirm_delete.html'
    success_url = reverse_lazy('account_logout')

    def test_func(self):
        return self.get_object() == self.request.user
    
    
class AdminDashboardView(LoginRequiredMixin, UserPassesTestMixin, TemplateView):
    template_name = 'users/admin_dashboard.html'

    def test_func(self):
        user = self.request.user
        return user.is_superuser or user.role == User.ADMIN 
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['total_users'] = User.objects.count()
        context['total_notes'] = Note.objects.count()
        context['active_users'] = User.objects.annotate(
            note_count=Count('note')
        ).filter(note_count__gt=0).order_by('-note_count')[:5]
        
        context['critical_logs'] = AuditLog.objects.filter(
            action__in=['LOGIN_FAIL', 'NOTE_DELETED_PERMANENTLY', 'ACCOUNT_DELETED']
        ).select_related('user').order_by('-timestamp')[:5] 
        
        return context
    
def admin_home_view(request):
    context = {} 
    return render(request, 'users/admin_home.html', context)

@login_required
def custom_redirect_view(request):
    if request.user.is_staff or request.user.is_superuser or request.user.role == 'admin':
        return redirect('users:admin_home')
    else:
        return redirect('notes:note_list')