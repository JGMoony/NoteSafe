from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.utils.html import format_html

from .forms import CustomUserCreationForm, CustomUserChangeForm

User = get_user_model()

class CustomUserAdmin(UserAdmin):

    add_form_template = 'admin/add_form.html'
    change_form_template = 'admin/change_form.html'
    delete_confirmation_template = 'admin/delete_confirmation.html'

    form = CustomUserChangeForm
    add_form = CustomUserCreationForm

    list_display = ('email', 'nombre', 'apellido', 'role', 'is_staff', 'is_active', 'actions_column') #
    list_display_links = ('email', 'nombre')
    list_filter = ('role', ('is_staff', admin.BooleanFieldListFilter), ('is_superuser', admin.BooleanFieldListFilter), ('is_active', admin.BooleanFieldListFilter))
    ordering = ('email',)
    search_fields = ('email', 'nombre', 'apellido')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('nombre', 'apellido', 'role')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser'),
            'classes': ('collapse',),
        }),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'nombre', 'apellido', 'role', 'password1', 'password2'), # Asegúrate de incluir 'role'
        }),
    )

    exclude = ('username',)

    def actions_column(self, obj):
        change_url = reverse(f'admin:{self.opts.app_label}_{self.opts.model_name}_change', args=[obj.pk])
        delete_url = reverse(f'admin:{self.opts.app_label}_{self.opts.model_name}_delete', args=[obj.pk])

        return format_html(
            '<a href="{}" class="btn btn-sm btn-ghost">Editar</a> &nbsp; <a href="{}" class="btn btn-sm btn-danger">Eliminar</a>',
            change_url,
            delete_url
        )
    actions_column.short_description = 'Acciones'

    def response_post_save_add(self, request, obj):
        messages.success(request, 'El usuario fue creado exitosamente.')

        changelist_url = reverse(f'admin:{self.opts.app_label}_{self.opts.model_name}_changelist')
        return HttpResponseRedirect(changelist_url)


admin.site.register(User, CustomUserAdmin)
