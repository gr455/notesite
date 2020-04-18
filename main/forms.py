from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, AbstractBaseUser
from django.db.models import UniqueConstraint
from .models import *
from tinymce.widgets import TinyMCE

class NewUserForm(UserCreationForm):

	email = forms.EmailField(required = True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

		def save(self, commit = True):
			user = super(NewUserForm, self).save(commit = False)
			user.email = self.cleaned_data.get('email')
			if commit:
				user.save()
			return user

class NoteForm(forms.ModelForm):
	note_chapter = forms.ModelChoiceField(queryset = Chapter.objects.all(), widget=forms.Select(attrs={'class':'browser-default'})) #because the trash materialize overrides the choicefield
	formfield_overrides = {
		models.TextField: {
							'widget': forms.Textarea(attrs={'rows':4, 'cols':40}),
							}
	}

	class Meta:
		model = Note
		fields = ["note_title","note_summary","note_chapter"]