from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseBadRequest
from .models import *
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth import login, logout, authenticate
from .forms import *
import hashlib 
from django.contrib import messages
from django.shortcuts import get_object_or_404, get_list_or_404
from django.core.exceptions import PermissionDenied
from django.core.files.storage import FileSystemStorage
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.conf import settings
from django.core.exceptions import SuspiciousOperation
import os


def homepage(request):
	logged_in = False
	course_count = range(0,Course.objects.count(),2)

	if request.user.is_authenticated:
		logged_in = True
	params = {"notes": Note.objects.order_by('-note_whenPublished')[:6],
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
			email = info.cleaned_data.get('email')
			if User.objects.filter(email = email).exists():
				info.add_error('email', 'account with email already exists')
				err_msgs = info.errors.items
			else:
				user = info.save()
				user.is_active = False
				user.save()
				hashed = make_hash(user)
				send_mail("Notesite sign up confirmation",
				 		   f"Thank you {user.first_name} for registering with Notesite as {user.username}. Please click on the link below to activate your account \n\n {request.META['HTTP_HOST']}/users/validate/{user.username}/{hashed}",
				 		   settings.EMAIL_HOST_USER,
				 		   [user.email,])
				return redirect("/preconfirm")
		else:
			err_msgs = info.errors.items

	create_form = NewUserForm
	return render(request = request,
				  template_name = "main/register.html",
				  context = {"create_form": create_form,
				  			 "err_msgs": err_msgs})

#TODO: not be lazy and make a proper digest
def make_hash(user):
	hash =  hashlib.sha256(str.encode(user.username+user.password)).hexdigest()
	return hash

def activate_user(request, username, token):
	user = get_object_or_404(User, username = username)
	valid_token = make_hash(user)

	if not user.is_active and valid_token == token:
		user.is_active = True
		user.save()
		messages.success(request, f"User confirmation successful. Please login to proceed")
		return redirect('/login')
	else:
		return HttpResponse("The link is incorrect or the user is already validated")

def preconfirm(request):

	if request.user.is_active:
		messages.success(request, f"Account already activated")
		return redirect('/')

	return render(request = request,
				  template_name = "main/preconfirm.html",
				  context = {"logged_in": False})

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
			if user and user.is_active:
				messages.success(request, f"Logged in")
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
	if request.method == 'POST':
		if not request.user.username == note.note_author:
			return PermissionDenied
		else:
			if os.path.isfile(os.path.join(settings.MEDIA_ROOT, note.note_fileurl.split('/')[-1])):
				os.remove(os.path.join(settings.MEDIA_ROOT, note.note_fileurl.split('/')[-1]))
			note.delete()
			messages.success(request, f"Note Deleted")
			return redirect("/")


	return render(request = request,
				  template_name = "main/show.html",
				  context = {"course": course,
				  			 "chapter": chapter,
				  			 "note": note,
				  			 "file_type": note.note_fileurl.split('.')[-1],
				  			 "logged_in": logged_in})

def open_document(request, var, var2, var3):
	return HttpResponse(200)

def create(request):
	err_msgs = None
	permitted_extensions = ['png','jpg','jpeg','pdf','odf','docx','doc','ppt','txt']
	illegal_file_extension = False

	if not request.user.is_authenticated:
		raise PermissionDenied

	logged_in = True
	if request.method == "POST":
		data = NoteForm(request.POST)
		note = data.save(commit = False)
		note.note_author = request.user
		chapter = data.cleaned_data.get('note_chapter')
		
		request_file = request.FILES['document'] if 'document' in request.FILES else None
		if request_file:
			if request_file.name.split('.')[-1] in permitted_extensions and request_file.size <= 5242880:

				fs = FileSystemStorage()
				file = fs.save(request_file.name, request_file)
				fileurl = fs.url(file)

				note.note_fileurl = fileurl
			else:
				illegal_file_extension = True

		if data.is_valid() and not illegal_file_extension:
			note.save()
			messages.success(request, f"Note published")
			return redirect(f"/{chapter.chapter_course.course_code}/{chapter.chapter_name}/{note.id}")
		
		#todo notification about publishing
		else:
			err_msgs = data.errors.items


	new_form = NoteForm
	return render(request = request,
		          template_name = "main/new.html",
		          context = {"new_form": new_form,
		          			 "logged_in": logged_in,
		          			 "err_msgs": err_msgs,
		          			 "illegal_extension": illegal_file_extension})

def view_user(request, uname):
	if not request.user.is_authenticated:
		pass

	query_user = get_object_or_404(User, username = uname) 

	curr_user = request.user
	user_is_authenticated = False
	if curr_user.username == uname:
		user_is_authenticated = True

	user_notes = Note.objects.filter(note_author = uname)

	return render(request = request,
				  template_name = "main/user.html",
				  context = {"logged_in": request.user.is_authenticated,
				  			 "query_user": query_user,
				  			 "curr_user_is_auth": user_is_authenticated,
				  			 "notes": user_notes})

def user_settings(request, uname):
	if request.user.username != uname:
		return PermissionDenied

	user = request.user

	if request.method == "POST":
		action = request.POST.copy().get('act')
		if action == "chname":
			pass
		elif action == "chpass":
			pass
		elif action == "deac":
			return HttpResponse(200)
		else:
			return HttpResponseBadRequest("400 Bad Request")


	return render(request = request,
				  template_name = "main/user_settings.html",
				  context = {"user": user,
				  			 "logged_in": user.is_authenticated},)