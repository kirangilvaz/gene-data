from django.http import HttpResponse,HttpResponseRedirect
import sys
from django.shortcuts import render_to_response
#from gene.models import *
from django.template import Context, loader
from django.core.context_processors import csrf
from utility import handle_uploaded_file
sys.stdout=sys.stderr

def upload(request):
	c={}
	c.update(csrf(request))
	varData="Kiran"
	template=loader.get_template('../templates/upload.html')
	#context=Context({'varData':varData})
	#return HttpResponse(template.render(context))
	return render_to_response('../templates/upload.html',c)

def index(request):
	return HttpResponse('Hello Universe!')

def FileUpload(request):
	if request.method=='POST':
		fileObj=request.FILES['file']
		email=str(request.POST.get('email'))
		handle_uploaded_file(fileObj,email)
		return HttpResponse("You file has been uploaded. Your data will be emailed to you at "+email+" as soon as we have processed your request.")
	return HttpResponse('Sorry. Something went wrong')
