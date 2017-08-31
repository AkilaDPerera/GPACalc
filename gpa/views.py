from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse

from . import LOGIC
from . import emailClient as ec

from django.contrib.auth.models import User
from gpa.models import Profile
from gpa.models import Semester
from gpa.models import Performance
from gpa.models import Module
from gpa.models import Feedback
from gpa.models import MarkSheet

import json
    
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
                
                #Inform admin
                subject = "[NEW USER] " + user.username + "-" + user.first_name + " has registered to the system"
                message = "Username: " + user.username + "\nFirst Name: " + user.first_name
                ec.send(subject, message)
                
                user = authenticate(username=index, password=psswrd)
                
                #Setup profile
                profile = Profile(user=user, fullName=name, count=0)
                profile.save()
        
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
    
    #get visited count
    profile.count += 1
    profile.save() #To update the time
    
    #Handling admin msg
    if not(profile.is_msg_showed):
        profile.is_msg_showed=True
        profile.save()
        profile.is_msg_showed=False
    
    scoreEntires = Performance.objects.filter(user=user)
    performance = LOGIC.GETPERFORMANCE(scoreEntires)
    semGPAs, overallBest, overallCorrect, sem_list = LOGIC.GETGPAS(performance)
    class_no, class_name = LOGIC.GETCLASS(overallCorrect)
    
    #Feedback process
    reviewList = Feedback.objects.all().order_by('-date')[:10]

    reviews = []
    for review in reviewList:
        rl = dict()
        rl["id"] = review.id
        rl["user"] = review.user.first_name
        rl["index"] = review.user.username
        rl["message"] = review.message
        rl["rate"] = "*"*review.rate
        rl["date"] = str(review.date.date())
        rl["time"] = str(review.date.time())
        if (request.user==review.user):
            rl["isDeleteEnable"] = True;
        else:
            rl["isDeleteEnable"] = False;
        reviews.append(rl)

    possibleGrades = ["UNKNOWN", "Non-GPA", "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]

    return render(request, 'gpa/auto/profile.html', {'last_viewed':user.last_login.date(), 'profile':profile, "correctGPA":overallCorrect, "actualGPA":overallBest, "className":class_name, "class_no":class_no, "semList":sem_list, "SGPA":semGPAs, "performance":performance, "possibleGrades":possibleGrades, "reviews":reviews})

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

def postReview(request):
    data = dict(request.POST)
    del data["csrfmiddlewaretoken"]
    user = request.user
    
    feedback = Feedback(user=user, rate=int(data["rate"][0]), message=data["message"][0])
    feedback.save()
    
    #Inform admin
    subject = "[ADD REVIEW] " + user.username + "-" + user.first_name + " has posted review"
    message = "Rate: " + str(data["rate"][0]) +"\nMessage:\n\t" + data["message"][0]
    ec.send(subject, message)
    
    #Retrieve data sorted by date
    reviewList = Feedback.objects.all().order_by('-date')[:10]

    list = []
    for review in reviewList:
        rl = dict()
        rl["id"] = review.id
        rl["user"] = review.user.first_name
        rl["index"] = review.user.username
        rl["message"] = review.message
        rl["rate"] = review.rate
        rl["date"] = str(review.date.date())
        rl["time"] = str(review.date.time())
        if (request.user==review.user):
            rl["isDeleteEnable"] = True;
        else:
            rl["isDeleteEnable"] = False;
        list.append(rl)

    return HttpResponse(json.dumps(list), content_type="application/json")

def deleteReviews(request):
    data = dict(request.POST)
    id = data["id"][0]
    review = Feedback.objects.get(id=id)
    
    if (review.user==request.user):
        review.delete()
        
    #Inform admin
    subject = "[DELETE REVIEW] " + review.user.username + "-" + review.user.first_name + " has deleted review"
    message = "Rate was: " + str(review.rate) +"\nMessage was:\n\t" + review.message
    ec.send(subject, message)

    #Retrieve data sorted by date
    reviewList = Feedback.objects.all().order_by('-date')[:10]

    list = []
    for review in reviewList:
        rl = dict()
        rl["id"] = review.id
        rl["user"] = review.user.first_name
        rl["index"] = review.user.username
        rl["message"] = review.message
        rl["rate"] = review.rate
        rl["date"] = str(review.date.date())
        rl["time"] = str(review.date.time())
        if (request.user==review.user):
            rl["isDeleteEnable"] = True;
        else:
            rl["isDeleteEnable"] = False;
        list.append(rl)

    return HttpResponse(json.dumps(list), content_type="application/json")
    
def getMarkSheetURLs(request):
    data = dict(request.POST)
    
    user = request.user
    batch = user.username[:2]
    possibleURLs = MarkSheet.objects.filter(batch=batch)

    output = []
    for module in data['modules[]']:
        out=[]
        sheetInfo = ""
        
        mod = Module.objects.get(moduleCode=module)
        specificModule = possibleURLs.filter(module=mod)
        
        # Non gpa label handling
        isNonGPALabelAvailable = False
        # admin's idea
        if(mod.isNonGPA):
            percentage = "100.0"
            isNonGPALabelAvailable = True
        else:
            perfRecords = Performance.objects.filter(module=mod)
            nonGPACount = len(perfRecords.filter(grade="Non-GPA"))
            unknownCount = len(perfRecords.filter(grade="UNKNOWN"))
            totCount = len(perfRecords)
            percentage = nonGPACount*100/(totCount-unknownCount+1)
            if((totCount-unknownCount)>9) and (percentage>79): #REMEMBER TO CHANGE THIS IN PRODUCTION
                percentage = "%.1f"%(percentage)
                isNonGPALabelAvailable = True
        
        if len(specificModule)==0:
            sheetInfo = MarkSheet(module=mod, batch=batch, user_requested=user)
            sheetInfo.save()
        else:
            sheetInfo = specificModule[0]

        out = [module, sheetInfo.status, sheetInfo.user_requested.username==user.username, sheetInfo.myUrl, isNonGPALabelAvailable, percentage]
        output.append(out)
        
    return HttpResponse(json.dumps(output), content_type="application/json")

def submitURL(request):
    data = dict(request.POST)

    user = request.user
    batch = user.username[:2]
    mod = data["moduleCode"][0]
    pendingURL = data["pendingURL"][0]
    
    module = Module.objects.get(moduleCode=mod)
    markSheet = MarkSheet.objects.get(module=module, batch=batch)
    
    markSheet.user_requested = user
    markSheet.pendingUrl = pendingURL
    
    if (markSheet.status=="NW"):
        markSheet.status = "PD"
    elif (markSheet.status=="VWAD"):
        markSheet.status="VWADPD"
        
    markSheet.save()
    
    #Send email to admin
    gotoURL = "https://akiladperera.alwaysdata.net/admin/gpa/marksheet/%d/change/"%(markSheet.id)
    subject = "[ADD URL] " + module.moduleCode + " | " + str(markSheet.batch) + " | " + user.username + "-" + user.first_name + " has added URL to admin approval"
    message = "Module code: " + module.moduleCode + "\tBatch: " + str(markSheet.batch) + "\nModule Name: " + module.moduleName + "\nModule Credits: " + str(module.credit) + "\nRequested By: " + user.username + "-" + user.first_name + "\nCurrent URL: " + markSheet.myUrl + "\nRequested URL to approval: " + markSheet.pendingUrl
    message += "\nGoto: " + gotoURL
    ec.send(subject, message)
         
    output = [markSheet.status, mod]
    return HttpResponse(json.dumps(output), content_type="application/json")

def cancelURL(request):
    data = dict(request.POST)
    user = request.user
    batch = user.username[:2]
    mod = data["moduleCode"][0]
    choice = data["currentStatus"][0]
    
    module = Module.objects.get(moduleCode=mod)
    markSheet = MarkSheet.objects.get(module=module, batch=batch)
    
    if choice=="PD":
        markSheet.status = "NW"
    elif choice=="VWADPD":
        markSheet.status = "VWAD"
    
    markSheet.save()
    
    #Send email to admin
    subject = "[DELETE URL] " + module.moduleCode + " | " + str(markSheet.batch) + " | "  + user.username + "-" + user.first_name + " has deleted URL"
    message = "Module code: " + module.moduleCode + "\tBatch: " + str(markSheet.batch) + "\nModule Name: " + module.moduleName + "\nModule Credits: " + str(module.credit) + "\nRequested By: " + user.username + "-" + user.first_name + "\nCurrent URL: " + markSheet.myUrl + "\nRequested URL to approval: " + markSheet.pendingUrl
    ec.send(subject, message)
    
    output = [markSheet.status]
    return HttpResponse(json.dumps(output), content_type="application/json")