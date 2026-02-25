from django.utils import timezone
from datetime import timedelta
from ..models import ClassJoinToken

def generate_join_token(virtual_class, user):
    return ClassJoinToken.objects.create(
        virtual_class=virtual_class,
        user=user,
        expires_at=timezone.now() + timedelta(minutes=15)
    )

