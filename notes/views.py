from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.db.models import Q
from .models import Note, AuditLog, Tag
from .forms import NoteForm


# LISTADO DE NOTAS
class NoteListView(LoginRequiredMixin, ListView):
    model = Note
    template_name = 'notes/note_list.html'
    context_object_name = 'notes'

    def get_queryset(self):
        queryset = Note.objects.filter(user=self.request.user)
        query = self.request.GET.get('q')
        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
        return queryset.order_by('-important', '-updated_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


# PROCESAMIENTO DE ETIQUETAS
def process_tags(user, note, new_tags_string):
    if not new_tags_string:
        return
    tag_names = [name.strip().lower() for name in new_tags_string.split(',') if name.strip()]
    for tag_name in tag_names:
        tag, _ = Tag.objects.get_or_create(name=tag_name, user=user)
        note.tags.add(tag)


# DETALLE DE NOTA
class NoteDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Note
    template_name = 'notes/note_detail.html'

    def test_func(self):
        return self.get_object().user == self.request.user


# CREACIÓN DE NOTA
class NoteCreateView(LoginRequiredMixin, CreateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'
    success_url = reverse_lazy('notes:note_list')
    def get_form_kwargs(self):
        """ Pasa el usuario actual al constructor del formulario """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Inyecta el usuario
        return kwargs

    def form_valid(self, form):
        form.instance.user = self.request.user
        response = super().form_valid(form)
        process_tags(self.request.user, form.instance, form.cleaned_data.get('new_tags'))
        AuditLog.objects.create(
            user=self.request.user,
            action="NOTE_CREATED",
            note_title=form.instance.title,
        )
        return response


# EDICIÓN DE NOTA
class NoteUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Note
    form_class = NoteForm
    template_name = 'notes/note_form.html'

    def get_form_kwargs(self):
        """ Pasa el usuario actual al constructor del formulario """
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user  # Inyecta el usuario
        return kwargs

    def get_success_url(self):
        return reverse_lazy('notes:note_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        response = super().form_valid(form)
        process_tags(self.request.user, form.instance, form.cleaned_data.get('new_tags'))
        AuditLog.objects.create(
            user=self.request.user,
            action="NOTE_EDITED",
            note_title=form.instance.title,
        )
        return response


# ELIMINACIÓN DE NOTA
class NoteDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Note
    template_name = 'notes/note_confirm_delete.html'
    success_url = reverse_lazy('notes:note_list')

    def test_func(self):
        return self.get_object().user == self.request.user

    def form_valid(self, form):
        note_title = self.object.title
        response = super().form_valid(form)
        AuditLog.objects.create(
            user=self.request.user,
            action="NOTE_DELETED",
            note_title=note_title,
        )
        return response


# HISTORIAL DE AUDITORÍA
class AuditLogListView(LoginRequiredMixin, ListView):
    model = AuditLog
    template_name = 'notes/audit_log.html'
    context_object_name = 'logs'
    paginate_by = 10

    def get_queryset(self):
        return AuditLog.objects.filter(user=self.request.user).order_by('-timestamp')