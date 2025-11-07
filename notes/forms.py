from django import forms
from .models import Note

class NoteForm(forms.ModelForm):
    
    new_tags = forms.CharField(
        max_length=25,
        required=False,
        label="Agregar nuevas etiquetas separadas por comas.",
        help_text='Ejemplo: trabajo, personal, urgente',
    )
    
    class Meta:
        model = Note
        fields = ['title', 'content', 'important', 'tags', 'new_tags'] 