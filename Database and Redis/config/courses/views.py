from django.core.cache import cache
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Course
from .serializers import CourseSerializer

class CourseDetailView(APIView):
    def get(self, request, course_id):
        cache_key = f'course_{course_id}_full'
        cached_data = cache.get(cache_key)
        
        if cached_data:
            return Response(cached_data)
        
        course = get_object_or_404(Course.objects.prefetch_related(
            'chapters__topics__subtopics__segments__contents__highlighted_words',
            'chapters__topics__subtopics__segments__contents__questions',
            'chapters__topics__subtopics__segments__contents__images'
        ), pk=course_id)
        
        serializer = CourseSerializer(course)
        cache.set(cache_key, serializer.data, timeout=60*60)  # Cache for 1 hour
        return Response(serializer.data)