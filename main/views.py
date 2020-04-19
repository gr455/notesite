from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from .forms import *
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage


def homepage(request):
	logged_in = False
	course_count = range(0,Course.objects.count(),2)

	if request.user.is_authenticated:
		logged_in = True
	params = {"notes": Note.objects.all,
			  "tutorials": Tutorial.objects.all,
			  "chapters": Chapter.objects.all,
			  "courses": Course.objects.all,
			  "logged_in": logged_in,
			  "range": course_count }
	return render(request = request,
				  template_name = "main/index.html",
				  context = params )


#Session Handling
def register(request):
	#send home if already logged in
	if request.user.is_authenticated:
		return redirect("/")

	err_msgs = None
	if request.method == "POST":
		info = NewUserForm(request.POST)
		if info.is_valid():
			user = info.save()
			login(request, user)
			return redirect("/")
		else:
			err_msgs = info.errors.items

	create_form = NewUserForm
	return render(request = request,
				  template_name = "main/register.html",
				  context = {"create_form": create_form,
				  			 "err_msgs": err_msgs})

def login_user(request):
	if request.user.is_authenticated:
		return redirect("/")
	err_msgs = None
	if request.method == "POST":
		info = AuthenticationForm(request, request.POST)
		if info.is_valid():
			username = info.cleaned_data.get('username')
			password = info.cleaned_data.get('password')
			user = authenticate(username = username, password = password)
			if user:
				login(request, user)
				return redirect("/")

		err_msgs = info.errors.items 

	login_form = AuthenticationForm()
	return render(request = request,
				  template_name = "main/login.html",
				  context = {"login_form":login_form,
				  			 "err_msgs": err_msgs})

def logout_user(request):
	if request.user.is_authenticated:
		logout(request)
		messages.info(request, "Logged out successfully")
	return redirect("/")

def direct_path(request, var):
	logged_in = False
	if request.user.is_authenticated:
		logged_in = True
	course = get_object_or_404(Course, course_code = var)
	chapters = Chapter.objects.filter(chapter_course = course)

	return render(request = request,
		          template_name = "main/chapters.html",
		          context = {"chapters": chapters,
		          			 "course": var,
		          			 "logged_in": logged_in})


def indirect_path(request, var, var2):

	logged_in = False
	if request.user.is_authenticated:
		logged_in = True
	course = get_object_or_404(Course, course_code = var)
	chapter = get_object_or_404(Chapter, chapter_course = course, chapter_name = var2)
	notes = Note.objects.filter(note_chapter = chapter)

	return render(request = request,
				  template_name = "main/notes.html",
				  context = {"notes": notes,
				  			 "logged_in":logged_in,
				  			 "chapter":chapter,
				  			 "course":course})


def show(request, var, var2, var3):
	logged_in = False
	if request.user.is_authenticated:
		logged_in = True
	course = get_object_or_404(Course, course_code = var)
	chapter = get_object_or_404(Chapter, chapter_course = course, chapter_name = var2)
	note = get_object_or_404(Note, note_chapter = chapter, id = var3)
	return render(request = request,
				  template_name = "main/show.html",
				  context = {"course": course,
				  			 "chapter": chapter,
				  			 "note": note,
				  			 "logged_in": logged_in})

def open_document(request, var, var2, var3):
	return HttpResponse(200)

def create(request):
	err_msgs = None
	if not request.user.is_authenticated:
		raise PermissionDenied

	logged_in = True
	if request.method == "POST":
		data = NoteForm(request.POST)
		note = data.save(commit = False)
		note.note_author = request.user
		
		request_file = request.FILES['document'] if 'document' in request.FILES else None
		if request_file:
			fs = FileSystemStorage()
			file = fs.save(request_file.name, request_file)
			fileurl = fs.url(file)
			print(fileurl)

			note.note_fileurl = fileurl

		if data.is_valid():
			note.save()
			redirect("/")
		
		#todo notification about publishing
		else:
			err_msgs = data.errors.items


	new_form = NoteForm
	return render(request = request,
		          template_name = "main/new.html",
		          context = {"new_form": new_form,
		          			 "logged_in": logged_in,
		          			 "err_msgs": err_msgs})