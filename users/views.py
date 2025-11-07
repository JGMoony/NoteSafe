from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import UpdateView, DetailView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.db.models import Count
from notes.models import Note, Tag
from .forms import ProfileUpdateForm

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
    
    
# ELIMINACIÓN DE PERFIL
class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = User
    template_name = 'users/profile_confirm_delete.html'
    success_url = reverse_lazy('account_logout')

    def test_func(self):
        return self.get_object() == self.request.user