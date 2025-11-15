from django import forms
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import pytz

User = get_user_model()

class CustomSignupForm(SignupForm):
    nombre = forms.CharField(max_length=100, label='Nombre')
    apellido = forms.CharField(max_length=100, label='Apellido', required=False)

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)


        user.nombre = self.cleaned_data['nombre']
        user.apellido = self.cleaned_data['apellido']
        user.save()
        return user


class ProfileUpdateForm(forms.ModelForm):
    timezone = forms.ChoiceField(
        choices=[(tz, tz) for tz in pytz.common_timezones],
        initial='America/Bogota',
        label='Zona horaria'
    )
    class Meta:
        model = User
        fields = ['nombre', 'apellido', 'timezone', 'theme']




class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email', 'nombre', 'apellido', 'role')
        exclude = ('username',)
        fields = ('email', 'nombre', 'apellido', 'role')
        exclude = ('username',)
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = '__all__'
