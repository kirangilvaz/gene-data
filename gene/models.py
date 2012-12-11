from django.db import models
from django import forms

class UploadFileForm(forms.Form):
	fileData = forms.FileField()


