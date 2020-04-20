from django.contrib.auth.models import User
from django.db import models
import django.utils


class Course(models.Model):
	course_name = models.CharField(max_length = 200)
	course_code = models.CharField(max_length = 8)

	def __str__(self):
		return self.course_code+" "+self.course_name

class Chapter(models.Model):

	chapter_no = models.PositiveIntegerField()
	chapter_name = models.CharField(max_length = 200)
	chapter_course = models.ForeignKey(Course,
									   default = 0,
									   verbose_name = "Course",
									   on_delete = models.CASCADE)
	def __str__(self):
		return str(self.chapter_course.course_code)+" "+ str(self.chapter_name)

class Note(models.Model):
	note_title = models.CharField(max_length = 200)
	note_summary = models.TextField(default = "", blank = True)
	note_whenPublished = models.DateTimeField("Date Published", default = django.utils.timezone.now)
	note_chapter = models.ForeignKey(Chapter,
									 default = 0,
									 verbose_name = "Chapter",
									 on_delete = models.CASCADE)
	note_author = models.CharField(max_length = 200, default = "")
	note_fileurl = models.CharField(max_length = 200, default = "", blank = True)

	def __str__(self):
		return str(self.id) +" "+ self.note_title

class Tutorial(models.Model):
	tutorial_title = models.CharField(max_length = 200)
	tutorial_content = models.TextField()
	tutorial_whenPublished = models.DateTimeField("Date Published", default = django.utils.timezone.now)
	tutorial_chapter = models.ForeignKey(Chapter,
										 default = 0,
										 verbose_name = "Chapter",
										 on_delete = models.CASCADE)

