from django.shortcuts import render
from django.shortcuts import HttpResponse
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


    
def choice2(request):
    
    if request.method=='POST':
        
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
    
        
        LOGIC.ADDINGGRADE(moduleList, request.POST)
        GPA = LOGIC.CALCGPA(moduleList)
        
        return render(request, 'calc/successFinal.html', {'semester':semChoice, 'name':realName, 'index':indexNumber, 'modules':moduleList, 'GPA':GPA})

            
        


	
