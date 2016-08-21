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

        #Serializing
        pickle_out = open('data.pickle', 'wb')
        pickle.dump({'realName':realName, 'indexNumber':indexNumber, 'semesters':semesters}, pickle_out)
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

        #OBJ de-serailization
        pickle_in = open('data.pickle', 'rb')
        data = pickle.load(pickle_in)
        pickle_in.close()

        semChoice = 'BSc Eng. Semester - '+ str(request.POST["semester"])
        data['semChoice'] = semChoice

        #OBJ Serialization
        pickle_out = open('data.pickle', 'wb')
        pickle.dump(data, pickle_out)
        pickle_out.close()

        #OBJ de-serailization
        pickle_in = open('data.pickle', 'rb')
        data = pickle.load(pickle_in)
        pickle_in.close()

        moduleList = data['semesters'][data['semChoice']]
        moduleList.sort(key=lambda x: x.credit, reverse=True)

        
    
        return render(request, 'calc/successSecond.html', {'semester':data['semChoice'], 'name':data['realName'], 'index':data['indexNumber'], 'modules':moduleList})
    else:
        return redirect('/calc/signin/')

    
def choice2(request):
    
    if request.method=='POST':

        #OBJ de-serailization
        pickle_in = open('data.pickle', 'rb')
        data = pickle.load(pickle_in)
        pickle_in.close()
        
        req = request.POST
        data['req'] = request.POST
        
        #OBJ Serialization
        pickle_out = open('data.pickle', 'wb')
        pickle.dump(data, pickle_out)
        pickle_out.close()
        
        #OBJ de-serailization
        pickle_in = open('data.pickle', 'rb')
        data = pickle.load(pickle_in)
        pickle_in.close()

    

        moduleList = data['semesters'][data['semChoice']]
        moduleList.sort(key=lambda x: x.credit, reverse=True)
    
        
        LOGIC.ADDINGGRADE(moduleList, data['req'])
        GPA = LOGIC.CALCGPA(moduleList)
        
        return render(request, 'calc/successFinal.html', {'semester':data['semChoice'], 'name':data['realName'], 'index':data['indexNumber'], 'modules':moduleList, 'GPA':GPA, 'post':Feedback.objects.order_by('-date')[:10]})

    else:
        return redirect('/calc/signin/')
    
    
def choice2_post(request):
    if request.method=='POST':
        
        if request.is_ajax():
            nameGiven = request.POST['name']
            comment = request.POST['message']
            
            #OBJ de-serailization
            pickle_in = open('data.pickle', 'rb')
            data = pickle.load(pickle_in)
            pickle_in.close()
            
            Feedback.objects.create(name=nameGiven, realName=data['realName'], index=data['indexNumber'], text=comment)

            
            
            moduleList = data['semesters'][data['semChoice']]
            moduleList.sort(key=lambda x: x.credit, reverse=True)
        
            
            LOGIC.ADDINGGRADE(moduleList, data['req'])
            GPA = LOGIC.CALCGPA(moduleList)
            
            
            
            return render(request, 'calc/successFinal.html', {'semester':data['semChoice'], 'name':data['realName'], 'index':data['indexNumber'], 'modules':moduleList, 'GPA':GPA, 'post':Feedback.objects.order_by('-date')[:10]})
    
    else:
        return redirect('/calc/signin/')
                

            
        


	
