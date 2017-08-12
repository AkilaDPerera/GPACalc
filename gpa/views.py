from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from . import LOGIC

from django.contrib.auth.models import User
from gpa.models import Profile
from gpa.models import Semester
from gpa.models import Performance
from gpa.models import Module

import json
from django.template.context_processors import request
    
def sign_in(request):
    if not(request.user.is_anonymous()):
        return get_profile(request)
    else:
        return render(request, "gpa/auto/auto.html")

def sign_out(request):
    logout(request) 
    return redirect("sign_in")

def get_profile(request):
    if (request.user.is_anonymous()):
        index = request.POST['index'].lower()
        psswrd = request.POST['password']
        
        name, indexNumber, semesters = LOGIC.SCRAPE(index, psswrd) #WEB Scraping
         
        if name==-1:
            #Incorrect password
            return render(request, 'gpa/auto/auto.html', {'class':'alert alert-danger fade in out', 'tag':'Attention!', 'message':'Wrong authentication information. Please check your username and password'})
        elif name==-2:
            # Exception occurs at login in both two tries
            return render(request, 'gpa/auto/auto.html', {'class':'alert alert-info fade in out', 'tag':'Information!', 'message':'Moodle denied the access. Please re-enter your authentication information of moodle and try again.'})
        elif name==-3:
            # lms web site structure was changed
            return render(request, 'gpa/auto/auto.html', {'class':'alert alert-info fade in out', 'tag':'Information!', 'message':'Moodle structure has been changed. You cannot use this service any longer. Thanks.'})
        else:
            #First try to authenticate
            user = authenticate(username=index, password=psswrd)
            if user is None:
                #Not registered user
                user = User.objects.create_user(index, 'no@email.set', psswrd)
                user.first_name = LOGIC.GETPETNAME(name)
                user.save()
                user = authenticate(username=index, password=psswrd)
                
                #Setup profile
                profile = Profile(user=user, fullName=name, count=0)
                profile.save()
            else:
                #Already registered user
                profile = Profile.objects.get(user=user)
                profile.count += 1
                profile.save() #To update the time

            #Now login
            login(request, user)
            
            #store the use full data now
            semesters=sorted(semesters.items(), key=lambda t:t[0], reverse=False)
            for semester in semesters:
                #add semester
                sem = Semester.objects.get_or_create(semesterName=semester[0])
                sem = sem[0]
                
                for module in sorted(semester[1], key=lambda t:t.getModuleCode()):
                    modu = Module.objects.get_or_create(moduleCode=module.getModuleCode(), moduleName=module.getModuleName(), credit=module.getModuleCredits())
                    modu = modu[0]
                    
                    #Create performance entries
                    performance = Performance.objects.get_or_create(user=user, module=modu, semester=sem)
            

    
    #User login now. I all requests request.user will be our user
    user = request.user
    profile = Profile.objects.get(user=user)
    scoreEntires = Performance.objects.filter(user=user)
    performance = LOGIC.GETPERFORMANCE(scoreEntires)
    semGPAs, overallBest, overallCorrect, sem_list = LOGIC.GETGPAS(performance)
    class_no, class_name = LOGIC.GETCLASS(overallCorrect)

    possibleGrades = ["UNKNOWN", "Non-GPA", "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]

    return render(request, 'gpa/auto/profile.html', {'last_viewed':user.last_login.date(), 'profile':profile, "correctGPA":overallCorrect, "actualGPA":overallBest, "className":class_name, "class_no":class_no, "semList":sem_list, "SGPA":semGPAs, "performance":performance, "possibleGrades":possibleGrades})

def submit(request):
    data = dict(request.POST)
    del data["csrfmiddlewaretoken"]
    
    user = request.user
    dbData = Performance.objects.filter(user=user)
    
    for name, value in data.items():
        mod = Module.objects.get(moduleCode=name)
        peformanceRecord = dbData.get(module=mod)
        peformanceRecord.grade = value[0]
        peformanceRecord.save()
    
    return HttpResponse(json.dumps({}), content_type="application/json")
    #send required data to refresh the page
#     profile = Profile.objects.get(user=user)
#     scoreEntires = Performance.objects.filter(user=user)
#     performance = LOGIC.GETPERFORMANCE(scoreEntires)
#     semGPAs, overallBest, overallCorrect, sem_list = LOGIC.GETGPAS(performance)
#     class_no, class_name = LOGIC.GETCLASS(overallCorrect)
# 
#     possibleGrades = ["UNKNOWN", "Non-GPA", "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]
#     return render(request, 'gpa/auto/profile.html', {'last_viewed':user.last_login.date(), 'profile':profile, "correctGPA":overallCorrect, "actualGPA":overallBest, "className":class_name, "class_no":class_no, "semList":sem_list, "SGPA":semGPAs, "performance":performance, "possibleGrades":possibleGrades})




