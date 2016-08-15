from django.shortcuts import render

def home(request):
	return render(request, 'personal/home.html')

def personal(request):
	return render(request, 'personal/personal.html')
	
def professional(request):
	return render(request, 'personal/professional.html')
	
def projects(request):
	return render(request, 'personal/projects.html')
	
def contact(request):
	return render(request, 'personal/contact.html')