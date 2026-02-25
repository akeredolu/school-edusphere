from django.shortcuts import render

from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from core.permissions import IsAdminUserRole
from attendance.models import PhysicalAttendance
from django.db.models import Count
from assignments.models import Assignment, Submission


@api_view(["GET"])
@permission_classes([IsAdminUserRole])
def attendance_report(request):
    data = (
        PhysicalAttendance.objects
        .values("classroom__name")
        .annotate(total=Count("id"))
        .order_by("-total")
    )

    return Response(data)



@api_view(["GET"])
@permission_classes([IsAdminUserRole])
def assignment_report(request):
    assignments = Assignment.objects.all()
    results = []

    for a in assignments:
        results.append({
            "title": a.title,
            "class": a.classroom.name,
            "submissions": a.submissions.count()  # use related_name
        })

    return Response(results)



from examinations.models import ExamResult
from django.db.models import Avg

@api_view(["GET"])
@permission_classes([IsAdminUserRole])
def performance_report(request):
    data = (
        ExamResult.objects
        .values("classroom__name")
        .annotate(avg_score=Avg("score"))
    )

    return Response(data)
