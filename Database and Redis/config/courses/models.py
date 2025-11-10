from django.db import models

# class Course(models.Model):
#     name = models.CharField(max_length=255)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name

# courses/models.py
class Course(models.Model):
    name = models.CharField(max_length=255)
    data_hash = models.CharField(max_length=64, blank=True)  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
class Chapter(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='chapters')
    chapter_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.name}"

class Topic(models.Model):
    chapter = models.ForeignKey(Chapter, on_delete=models.CASCADE, related_name='topics')
    topic_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.name}"

class SubTopic(models.Model):
    SUBTOPIC_TYPES = [
        ('Theory', 'Theory'),
        ('Practical', 'Practical'),
        ('Exercise', 'Exercise'),
    ]
    
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, related_name='subtopics')
    subtopic_id = models.CharField(max_length=50)
    name = models.CharField(max_length=255)
    subtopic_type = models.CharField(max_length=10, choices=SUBTOPIC_TYPES, default='Theory')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.order}. {self.name} ({self.subtopic_type})"

class Segment(models.Model):
    subtopic = models.ForeignKey(SubTopic, on_delete=models.CASCADE, related_name='segments')
    segment_id = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Segment {self.segment_id}"

class SegmentContent(models.Model):
    segment = models.ForeignKey(Segment, on_delete=models.CASCADE, related_name='contents')
    info_id = models.CharField(max_length=50)
    info = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Content {self.info_id}"

class HighlightedWord(models.Model):
    content = models.ForeignKey(SegmentContent, on_delete=models.CASCADE, related_name='highlighted_words')
    word = models.CharField(max_length=255)
    definition = models.TextField()

    def __str__(self):
        return self.word

class Question(models.Model):
    QUESTION_TYPES = [
        ('TrueFalse', 'True/False'),
        ('FillUps', 'Fill in the blanks'),
    ]
    
    DIFFICULTY_LEVELS = [
        ('Easy', 'Easy'),
        ('Medium', 'Medium'),
        ('Hard', 'Hard'),
    ]
    
    content = models.ForeignKey(SegmentContent, on_delete=models.CASCADE, related_name='questions')
    question_id = models.CharField(max_length=50)
    question_type = models.CharField(max_length=10, choices=QUESTION_TYPES)
    question = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_LEVELS, default='Easy')
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"{self.question_type} - {self.question[:50]}..."

class Image(models.Model):
    content = models.ForeignKey(SegmentContent, on_delete=models.CASCADE, related_name='images')
    image_path = models.CharField(max_length=255)
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.image_path