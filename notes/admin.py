from django.contrib import admin
from .models import Note, Tag, AuditLog

admin.site.register(Note)
admin.site.register(AuditLog)
admin.site.register(Tag) 
