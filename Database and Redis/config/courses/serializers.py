from rest_framework import serializers
from .models import *

class HighlightedWordSerializer(serializers.ModelSerializer):
    class Meta:
        model = HighlightedWord
        fields = ['word', 'definition']

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['question_id', 'question_type', 'question', 'answer', 'difficulty', 'order']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['image_path', 'alt_text']

class SegmentContentSerializer(serializers.ModelSerializer):
    highlighted_words = HighlightedWordSerializer(many=True)
    questions = QuestionSerializer(many=True)
    images = ImageSerializer(many=True)
    
    class Meta:
        model = SegmentContent
        fields = ['info_id', 'info', 'order', 'highlighted_words', 'questions', 'images']

class SegmentSerializer(serializers.ModelSerializer):
    contents = SegmentContentSerializer(many=True)
    
    class Meta:
        model = Segment
        fields = ['segment_id', 'order', 'contents']

class SubTopicSerializer(serializers.ModelSerializer):
    segments = SegmentSerializer(many=True)
    
    class Meta:
        model = SubTopic
        fields = ['subtopic_id', 'name', 'subtopic_type', 'order', 'segments']

class TopicSerializer(serializers.ModelSerializer):
    subtopics = SubTopicSerializer(many=True)
    
    class Meta:
        model = Topic
        fields = ['topic_id', 'name', 'order', 'subtopics']

class ChapterSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True)
    
    class Meta:
        model = Chapter
        fields = ['chapter_id', 'name', 'order', 'topics']

class CourseSerializer(serializers.ModelSerializer):
    chapters = ChapterSerializer(many=True)
    
    class Meta:
        model = Course
        fields = ['id', 'name', 'created_at', 'updated_at', 'chapters']