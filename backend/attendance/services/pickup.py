import random
from django.utils import timezone
from datetime import timedelta
from ..models import PickupCode

def generate_pickup_code(student, guardian):
    code = str(random.randint(100000, 999999))

    return PickupCode.objects.create(
        student=student,
        guardian=guardian,
        code=code,
        expires_at=timezone.now() + timedelta(hours=4)
    )

