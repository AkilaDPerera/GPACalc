from django.shortcuts import render, HttpResponse
import json

def home(request):
	return render(request, 'personal/home.html')

def personal(request):
	return render(request, 'personal/personal.html')
	
def professional(request):
	return render(request, 'personal/prof/index.html')
	
def projects(request):
	return render(request, 'personal/projects.html')
	
def contact(request):
	return render(request, 'personal/contact.html')

def getUser(request):
	if(request.user.is_anonymous()):
		data = {"user": "None"}
	else:
		data = {"user": request.user.username}
	
	return HttpResponse(json.dumps(data), content_type="application/json")

def error_404_view(request):
    return render(request, '404.html')
	