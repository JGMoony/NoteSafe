from django.dispatch import receiver
from allauth.account.signals import user_logged_in
from django.contrib.auth.signals import user_login_failed
from django.contrib.auth import get_user_model
from notes.models import AuditLog 

def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    AuditLog.objects.create(
        user=user,
        action="LOGIN_SUCCESS",
        ip_address=get_client_ip(request),
        extra=f"User {user.email} logged in successfully.",
    )

@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    User = get_user_model()
    try:
        user = User.objects.get(email=credentials.get('email'))
    except User.DoesNotExist:
        user = None
        
    AuditLog.objects.create(
        user=user if user else None, 
        action="LOGIN_FAILED",
        ip_address=get_client_ip(request),
        extra=f"Failed attempt for email: {credentials.get('email', 'N/A')}",
    )