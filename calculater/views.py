from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from . import LOGIC
from .LOGIC import ModuleToObject, ConnectPost, CalcGPA


user, sem, tot, modules, mod = None, None, None, None, None



def basic(request):
	return render(request, 'calc/basic.html')
	
def signin(request):
	return render(request, 'calc/signin_go.html')

def manual(request):
	return render(request, 'calc/manual.html')	

def btn1(request):
	global user, sem, tot, modules, mod
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password']
		
		user, sem, tot, mod = LOGIC.SCRAPE(username, password)
		
		if user==-2:
			return render(request, 'calc/signin_err.html')
		elif user==-1:
			return HttpResponse('Sorry, Internal error.')
		else:
			modules = LOGIC.ModuleToObject(mod)
			modules.sort(key=lambda x: x.GPAcredit, reverse=True)
			
			return render(request, 'calc/success.html', {'name':user[0], 'index':user[1], 'semester':sem[4:], 'total':tot, 'modules':modules})

def result(request):
	if request.method == 'POST':
		ConnectPost(modules, request.POST)
		currentGPA = round(CalcGPA(modules),4) 
		return render(request, 'calc/successNext.html', {'name':user[0], 'index':user[1], 'semester':sem[4:], 'total':tot, 'modules':modules, 'currentGPA':currentGPA})

	