from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # AUTH (COOKIE-BASED)
    path('api/v1/auth/', include('accounts.auth_urls')),

    # USERS
    path('api/v1/users/', include('accounts.user_urls')),

    # API v1 MODULES
    path('api/v1/schools/', include('schools.urls')),
    path('api/v1/students/', include('students.urls')),
    path('api/v1/teachers/', include('teachers.urls')),
    path('api/v1/parents/', include('parents.urls')),
    path('api/v1/academics/', include('academics.urls')),
    path('api/v1/materials/', include('materials.urls')),
    path('api/v1/examinations/', include('examinations.urls')),
    path('api/v1/virtual-classes/', include('virtual_classroom.urls')),
    path('api/v1/dashboard/', include('dashboard.urls')),
    path('api/v1/notifications/', include('notifications.urls')),
    path('api/v1/admin/', include('adminpanel.urls')),
    path('api/v1/reports/', include('reports.urls')),
]

