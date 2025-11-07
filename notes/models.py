from django.db import models
from django.conf import settings 

class Tag(models.Model): 
    name = models.CharField(max_length=50, unique=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 

    def __str__(self):
        return self.name
    
class Note(models.Model): 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    important = models.BooleanField(default=False) 
    tags = models.ManyToManyField(Tag, blank=True) 

    class Meta:
        ordering = ['-updated_at', '-created_at'] 

    def __str__(self):
        return self.title

class AuditLog(models.Model): 
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    action = models.CharField(max_length=100) 
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    extra = models.TextField(null=True, blank=True)
    note_title = models.CharField(max_length=100, null=True, blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email} - {self.action}"