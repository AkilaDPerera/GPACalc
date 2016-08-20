from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse

from calculater.models import Feedback
from . import LOGIC
import pickle




def basic(request):
    return render(request, 'calc/basic.html')
	
def signinPage(request):
    return render(request, 'calc/signin_normal.html')

def manual(request):
    return render(request, 'calc/manual.html')	

def signin(request):
    
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        realName, indexNumber, semesters = LOGIC.SCRAPE(username, password)
        
        #OBJ serializing
        pickle_out = open('realName.pickle', 'wb')
        pickle.dump(realName, pickle_out)
        pickle_out.close()
        
        pickle_out = open('indexNumber.pickle', 'wb')
        pickle.dump(indexNumber, pickle_out)
        pickle_out.close()
        
        pickle_out = open('semesters.pickle', 'wb')
        pickle.dump(semesters, pickle_out)
        pickle_out.close()
        
        
        #Handling error situations
        if realName==-2:
            return render(request, 'calc/signin_exception.html')
            
        elif realName==-1:
            return render(request, 'calc/signin_password.html')
        
        elif realName==-3:
            return HttpResponse("This service is no longer exist due to change of moodle structure. Sorry for the inconvenience.")
        
        else:
            #No errors things works as expected
            return render(request, 'calc/successFirst.html', {'petname':LOGIC.GETPETNAME(realName), 'semNo':LOGIC.GETSEMESTERDETECTION(semesters), 'semlist':LOGIC.GETSEMESTERLIST(semesters)})
    
    else:
        return redirect('/calc/signin/')
            
def choice1(request):
    
    if request.method=='POST':
        semChoice = 'BSc Eng. Semester - '+ str(request.POST["semester"])
        
        #OBJ Serialization
        pickle_out = open('semChoice.pickle', 'wb')
        pickle.dump(semChoice, pickle_out)
        pickle_out.close()

        #OBJ de-serailization
        pickle_in = open('realName.pickle', 'rb')
        realName = pickle.load(pickle_in)
        pickle_in.close()
        
        pickle_in = open('indexNumber.pickle', 'rb')
        indexNumber = pickle.load(pickle_in)
        pickle_in.close()
        
        pickle_in = open('semesters.pickle', 'rb')
        semesters = pickle.load(pickle_in)
        pickle_in.close()

        moduleList = semesters[semChoice]
        moduleList.sort(key=lambda x: x.credit, reverse=True)
    
        return render(request, 'calc/successSecond.html', {'semester':semChoice, 'name':realName, 'index':indexNumber, 'modules':moduleList})
        
    else:
        return redirect('/calc/signin/')

    
def choice2(request):
    
    if request.method=='POST':

        req = request.POST
        
        #Serialization
        pickle_out = open('request.pickle', 'wb')
        pickle.dump(req, pickle_out)
        pickle_out.close()
        
        
        #OBJ de-serailization
        pickle_in = open('realName.pickle', 'rb')
        realName = pickle.load(pickle_in)
        pickle_in.close()
        
        pickle_in = open('indexNumber.pickle', 'rb')
        indexNumber = pickle.load(pickle_in)
        pickle_in.close()
        
        pickle_in = open('semesters.pickle', 'rb')
        semesters = pickle.load(pickle_in)
        pickle_in.close()
        
        pickle_in = open('semChoice.pickle', 'rb')
        semChoice = pickle.load(pickle_in)
        pickle_in.close()


        moduleList = semesters[semChoice]
        moduleList.sort(key=lambda x: x.credit, reverse=True)

        LOGIC.ADDINGGRADE(moduleList, req) #Choice2
        GPA = LOGIC.CALCGPA(moduleList)
            
        return render(request, 'calc/successFinal.html', {'semester':semChoice, 'name':realName, 'index':indexNumber, 'modules':moduleList, 'GPA':GPA, 'post':Feedback.objects.order_by('-date')[:10]})

    else:
        return redirect('/calc/signin/')
    
    
def choice2_post(request):
    if request.method=='POST':
        
        if request.is_ajax():
            nameGiven = request.POST['name']
            comment = request.POST['message']

            Feedback.objects.create(name=nameGiven, realName=realName1, index=indexNumber, text=comment)
            
            #OBJ de-serailization
            pickle_in = open('request.pickle', 'rb')
            req = pickle.load(pickle_in)
            pickle_in.close()
            
            pickle_in = open('realName.pickle', 'rb')
            realName1 = pickle.load(pickle_in)
            pickle_in.close()
            
            pickle_in = open('indexNumber.pickle', 'rb')
            indexNumber = pickle.load(pickle_in)
            pickle_in.close()
            
            pickle_in = open('semesters.pickle', 'rb')
            semesters = pickle.load(pickle_in)
            pickle_in.close()
            
            pickle_in = open('semChoice.pickle', 'rb')
            semChoice = pickle.load(pickle_in)
            pickle_in.close()
            
            
    
            moduleList = semesters[semChoice]
            moduleList.sort(key=lambda x: x.credit, reverse=True)
        
            
            LOGIC.ADDINGGRADE(moduleList, req) #choice2_post
            GPA = LOGIC.CALCGPA(moduleList)
            
            return render(request, 'calc/successFinal.html', {'semester':semChoice, 'name':realName1, 'index':indexNumber, 'modules':moduleList, 'GPA':GPA, 'post':Feedback.objects.order_by('-date')[:10]})
    
    else:
        return redirect('/calc/signin/')
                

            
        


	
