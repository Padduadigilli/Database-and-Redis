# import json
# from django.core.management.base import BaseCommand
# from courses.models import Course, Chapter, Topic, SubTopic, Segment, SegmentContent, HighlightedWord, Question, Image

# class Command(BaseCommand):
#     help = 'Import course data from JSON file into the database'

#     def add_arguments(self, parser):
#         parser.add_argument(
#             'json_file',
#             type=str,
#             help='Path to the JSON file containing course data'
#         )
#         parser.add_argument(
#             '--clear',
#             action='store_true',
#             help='Clear existing data before import'
#         )

#     def handle(self, *args, **options):
#         json_file = options['json_file']
#         clear_existing = options['clear']

#         try:
#             with open(json_file, 'r') as f:
#                 data = json.load(f)
#         except FileNotFoundError:
#             self.stderr.write(self.style.ERROR(f"File not found: {json_file}"))
#             return
#         except json.JSONDecodeError:
#             self.stderr.write(self.style.ERROR(f"Invalid JSON in file: {json_file}"))
#             return

#         if clear_existing:
#             self.stdout.write(self.style.WARNING("Clearing existing course data..."))
#             Course.objects.all().delete()

#         # Create or update the course
#         course, created = Course.objects.update_or_create(
#             name=data['CourseName'],
#             defaults={}
#         )
#         action = "Created" if created else "Updated"
#         self.stdout.write(self.style.SUCCESS(f"{action} course: {course.name}"))

#         # Process chapters
#         for chapter_num, chapter_data in data['Chapters'].items():
#             chapter, created = Chapter.objects.update_or_create(
#                 course=course,
#                 chapter_id=chapter_data['ChapterID'],
#                 defaults={
#                     'name': chapter_data['ChapterName'],
#                     'order': int(chapter_num)
#                 }
#             )
#             self._process_topics(chapter, chapter_data['Topics'])

#         self.stdout.write(self.style.SUCCESS("Successfully imported course data"))

#     def _process_topics(self, chapter, topics_data):
#         for topic_num, topic_data in topics_data.items():
#             topic, created = Topic.objects.update_or_create(
#                 chapter=chapter,
#                 topic_id=topic_data['TopicID'],
#                 defaults={
#                     'name': topic_data['TopicName'],
#                     'order': int(topic_num)
#                 }
#             )
#             self._process_subtopics(topic, topic_data['SubTopics'])

#     def _process_subtopics(self, topic, subtopics_data):
#         for subtopic_num, subtopic_data in subtopics_data.items():
#             subtopic, created = SubTopic.objects.update_or_create(
#                 topic=topic,
#                 subtopic_id=subtopic_data['SubTopicID'],
#                 defaults={
#                     'name': subtopic_data['SubTopicName'],
#                     'subtopic_type': subtopic_data['SubTopicType'],
#                     'order': int(subtopic_num)
#                 }
#             )
#             self._process_segments(subtopic, subtopic_data['Segments'])

#     def _process_segments(self, subtopic, segments_data):
#         for segment_id, segment_contents in segments_data.items():
#             segment, created = Segment.objects.update_or_create(
#                 subtopic=subtopic,
#                 segment_id=segment_id,
#                 defaults={
#                     'order': int(segment_id[1:])  # Extract number from S1, S2, etc.
#                 }
#             )
#             self._process_segment_contents(segment, segment_contents)

#     def _process_segment_contents(self, segment, contents_data):
#         for content_data in contents_data:
#             content, created = SegmentContent.objects.update_or_create(
#                 segment=segment,
#                 info_id=content_data['InfoID'],
#                 defaults={
#                     'info': content_data['Info'],
#                     'order': int(content_data['InfoID'].split('-')[1])  # S1-1 → 1
#                 }
#             )
#             self._process_highlighted_words(content, content_data.get('HighlightedWords', {}))
#             self._process_questions(content, content_data.get('Questions', {}))
#             self._process_images(content, content_data)

#     def _process_highlighted_words(self, content, highlighted_words):
#         for word, definition in highlighted_words.items():
#             HighlightedWord.objects.update_or_create(
#                 content=content,
#                 word=word,
#                 defaults={'definition': definition}
#             )

#     def _process_questions(self, content, questions_data):
#         for question_type, questions in questions_data.items():
#             for question_data in questions:
#                 Question.objects.update_or_create(
#                     content=content,
#                     question_id=question_data['QuestionID'],
#                     defaults={
#                         'question_type': question_type,
#                         'question': question_data['Question'],
#                         'answer': question_data['Answer'],
#                         'difficulty': question_data['Type'],
#                         'order': int(question_data['QuestionID'].split('-')[1])  # T/F-1 → 1
#                     }
#                 )

#     def _process_images(self, content, content_data):
#         # Handle images if they exist in the content data
#         if 'img' in content_data:  # Adjust based on your actual image field
#             Image.objects.update_or_create(
#                 content=content,
#                 image_path=content_data['img'],
#                 defaults={'alt_text': ''}
#             )



import json
import redis
from django.conf import settings
from django.core.management.base import BaseCommand
from courses.models import Course, Chapter, Topic, SubTopic, Segment, SegmentContent, HighlightedWord, Question, Image

# Setup Redis connection
r = redis.Redis(host='localhost', port=6379, db=0)

class Command(BaseCommand):
    help = 'Import course data from JSON file into the database and Redis'

    def add_arguments(self, parser):
        parser.add_argument('json_file', type=str, help='Path to the JSON file containing course data')
        parser.add_argument('--clear', action='store_true', help='Clear existing data before import')

    def handle(self, *args, **options):
        json_file = options['json_file']
        clear_existing = options['clear']

        try:
            with open(json_file, 'r') as f:
                data = json.load(f)
        except FileNotFoundError:
            self.stderr.write(self.style.ERROR(f"File not found: {json_file}"))
            return
        except json.JSONDecodeError:
            self.stderr.write(self.style.ERROR(f"Invalid JSON in file: {json_file}"))
            return

        if clear_existing:
            self.stdout.write(self.style.WARNING("Clearing existing course data..."))
            Course.objects.all().delete()
            r.flushdb()

        course, created = Course.objects.update_or_create(
            name=data['CourseName'],
            defaults={}
        )
        action = "Created" if created else "Updated"
        self.stdout.write(self.style.SUCCESS(f"{action} course: {course.name}"))

        # Store course in Redis
        r.hset(f"course:{course.id}", mapping={"name": course.name})

        for chapter_num, chapter_data in data['Chapters'].items():
            chapter, created = Chapter.objects.update_or_create(
                course=course,
                chapter_id=chapter_data['ChapterID'],
                defaults={
                    'name': chapter_data['ChapterName'],
                    'order': int(chapter_num)
                }
            )
            r.hset(f"chapter:{chapter.id}", mapping={
                "chapter_id": chapter.chapter_id,
                "name": chapter.name,
                "order": chapter.order,
                "course_id": course.id
            })
            self._process_topics(chapter, chapter_data['Topics'])

        self.stdout.write(self.style.SUCCESS("Successfully imported course data"))

    def _process_topics(self, chapter, topics_data):
        for topic_num, topic_data in topics_data.items():
            topic, created = Topic.objects.update_or_create(
                chapter=chapter,
                topic_id=topic_data['TopicID'],
                defaults={
                    'name': topic_data['TopicName'],
                    'order': int(topic_num)
                }
            )
            r.hset(f"topic:{topic.id}", mapping={
                "topic_id": topic.topic_id,
                "name": topic.name,
                "order": topic.order,
                "chapter_id": chapter.id
            })
            self._process_subtopics(topic, topic_data['SubTopics'])

    def _process_subtopics(self, topic, subtopics_data):
        for subtopic_num, subtopic_data in subtopics_data.items():
            subtopic, created = SubTopic.objects.update_or_create(
                topic=topic,
                subtopic_id=subtopic_data['SubTopicID'],
                defaults={
                    'name': subtopic_data['SubTopicName'],
                    'subtopic_type': subtopic_data['SubTopicType'],
                    'order': int(subtopic_num)
                }
            )
            r.hset(f"subtopic:{subtopic.id}", mapping={
                "subtopic_id": subtopic.subtopic_id,
                "name": subtopic.name,
                "subtopic_type": subtopic.subtopic_type,
                "order": subtopic.order,
                "topic_id": topic.id
            })
            self._process_segments(subtopic, subtopic_data['Segments'])

    def _process_segments(self, subtopic, segments_data):
        for segment_id, segment_contents in segments_data.items():
            segment, created = Segment.objects.update_or_create(
                subtopic=subtopic,
                segment_id=segment_id,
                defaults={
                    'order': int(segment_id[1:])
                }
            )
            r.hset(f"segment:{segment.id}", mapping={
                "segment_id": segment.segment_id,
                "order": segment.order,
                "subtopic_id": subtopic.id
            })
            self._process_segment_contents(segment, segment_contents)

    def _process_segment_contents(self, segment, contents_data):
        for content_data in contents_data:
            content, created = SegmentContent.objects.update_or_create(
                segment=segment,
                info_id=content_data['InfoID'],
                defaults={
                    'info': content_data['Info'],
                    'order': int(content_data['InfoID'].split('-')[1])
                }
            )
            r.hset(f"content:{content.id}", mapping={
                "info_id": content.info_id,
                "info": content.info,
                "order": content.order,
                "segment_id": segment.id
            })
            self._process_highlighted_words(content, content_data.get('HighlightedWords', {}))
            self._process_questions(content, content_data.get('Questions', {}))
            self._process_images(content, content_data)

    def _process_highlighted_words(self, content, highlighted_words):
        for word, definition in highlighted_words.items():
            hw, _ = HighlightedWord.objects.update_or_create(
                content=content,
                word=word,
                defaults={'definition': definition}
            )
            r.hset(f"highlighted_word:{hw.id}", mapping={
                "word": word,
                "definition": definition,
                "content_id": content.id
            })

    def _process_questions(self, content, questions_data):
        for question_type, questions in questions_data.items():
            for question_data in questions:
                question, _ = Question.objects.update_or_create(
                    content=content,
                    question_id=question_data['QuestionID'],
                    defaults={
                        'question_type': question_type,
                        'question': question_data['Question'],
                        'answer': question_data['Answer'],
                        'difficulty': question_data['Type'],
                        'order': int(question_data['QuestionID'].split('-')[1])
                    }
                )
                r.hset(f"question:{question.id}", mapping={
                    "question_id": question.question_id,
                    "question_type": question.question_type,
                    "question": question.question,
                    "answer": question.answer,
                    "difficulty": question.difficulty,
                    "order": question.order,
                    "content_id": content.id
                })

    def _process_images(self, content, content_data):
        if 'img' in content_data:
            image, _ = Image.objects.update_or_create(
                content=content,
                image_path=content_data['img'],
                defaults={'alt_text': ''}
            )
            r.hset(f"image:{image.id}", mapping={
                "image_path": image.image_path,
                "alt_text": image.alt_text,
                "content_id": content.id
            })


