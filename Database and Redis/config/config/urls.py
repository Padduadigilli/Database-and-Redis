from django.contrib import admin
from django.urls import path
from courses.views import CourseDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/courses/<int:course_id>/', CourseDetailView.as_view(), name='course-detail'),
]