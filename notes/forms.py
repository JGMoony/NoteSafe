from django import forms
from .models import Note, Tag  # 👈 ¡Asegúrate de importar Tag!

class NoteForm(forms.ModelForm):
    
    new_tags = forms.CharField(
        max_length=25,
        required=False,
        label="Agregar nuevas etiquetas separadas por comas.",
        help_text='Ejemplo: trabajo, personal, urgente',
    )
    def __init__(self, *args, **kwargs):
        """
        Este método se ejecuta en cuanto se crea el formulario.
        """
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            self.fields['tags'].queryset = Tag.objects.filter(user=user)
    
    class Meta:
        model = Note
        fields = ['title', 'content', 'important', 'tags', 'new_tags']