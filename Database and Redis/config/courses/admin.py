from django.contrib import admin
from .models import *

class HighlightedWordInline(admin.TabularInline):
    model = HighlightedWord
    extra = 1

class QuestionInline(admin.TabularInline):
    model = Question
    extra = 1

class ImageInline(admin.TabularInline):
    model = Image
    extra = 1

class SegmentContentInline(admin.TabularInline):
    model = SegmentContent
    inlines = [HighlightedWordInline, QuestionInline, ImageInline]
    extra = 1

class SegmentInline(admin.TabularInline):
    model = Segment
    inlines = [SegmentContentInline]
    extra = 1

class SubTopicInline(admin.TabularInline):
    model = SubTopic
    inlines = [SegmentInline]
    extra = 1

class TopicInline(admin.TabularInline):
    model = Topic
    inlines = [SubTopicInline]
    extra = 1

class ChapterInline(admin.TabularInline):
    model = Chapter
    inlines = [TopicInline]
    extra = 1

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    inlines = [ChapterInline]

# Register other models if you want them to appear separately in admin
admin.site.register(Chapter)
admin.site.register(Topic)
admin.site.register(SubTopic)
admin.site.register(Segment)
admin.site.register(SegmentContent)
admin.site.register(HighlightedWord)
admin.site.register(Question)
admin.site.register(Image)