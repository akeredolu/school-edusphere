from django.conf import settings
from django.core.mail import send_mail
from notifications.models import Notification

def notify_students(classroom, assignment, send_email=False):
    """
    Notify all students in a classroom about a new assignment.
    Creates a Notification object for each student and optionally sends an email.
    
    Args:
        classroom: Classroom instance with 'students' related_name
        assignment: Assignment instance
        send_email: If True, sends an email to each student
    """
    students = classroom.students.all()  # queryset of Student or related object

    for student in students:
        # Create Notification
        Notification.objects.create(
            recipient=student.user,  # User instance
            title="New Assignment",
            message=f"{assignment.title} has been posted.",
            notification_type="assignment",  # matches your model field
            delivery_channel="push"  # default delivery channel
        )

        # Optionally send email
        if send_email and student.user.email:
            send_mail(
                subject="New Assignment",
                message=f"Hi {student.user.get_full_name()},\n\n"
                        f"A new assignment '{assignment.title}' has been posted in your class.",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[student.user.email],
            )
