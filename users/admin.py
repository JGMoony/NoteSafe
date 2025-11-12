from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserCreationForm, CustomUserChangeForm 

User = get_user_model()

class CustomUserAdmin(UserAdmin):
    
    add_form_template = 'admin/add_form.html'
    
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm 
    
    list_display = ('email', 'nombre', 'apellido', 'role', 'is_staff', 'is_active')
    list_display_links = ('email', 'nombre') 
    list_filter = ('role', ('is_staff', admin.BooleanFieldListFilter), ('is_superuser', admin.BooleanFieldListFilter), ('is_active', admin.BooleanFieldListFilter))
    ordering = ('email',) 
    search_fields = ('email', 'nombre', 'apellido')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}), 
        ('Información Personal', {'fields': ('nombre', 'apellido', 'timezone', 'theme')}),
        ('Permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'role', 'groups', 'user_permissions')}),
        ('Fechas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'apellido', 'password', 'password2'),
        }),
    )
    
    exclude = ('username',) 


admin.site.register(User, CustomUserAdmin)