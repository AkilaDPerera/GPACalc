from django.shortcuts import render
from django.shortcuts import HttpResponse
from . import LOGIC

#User inputs as variables
semChoice = ''

#General variables
realName, indexNumber, semesters = None, None, None

def basic(request):
	return render(request, 'calc/basic.html')
	
def signinPage(request):
	return render(request, 'calc/signin_normal.html')

def manual(request):
	return render(request, 'calc/manual.html')	

def signin(request):
    global realName, indexNumber, semesters
    
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        
        realName, indexNumber, semesters = LOGIC.SCRAPE(username, password)
        
        #Handling error situations
        if realName==-2:
            return render(request, 'calc/signin_exception.html')
            
        elif realName==-1:
            return render(request, 'calc/signin_password.html')
        
        elif realName==-3:
            return HttpResponse("This service is no longer exist due to change of moodle structure. Sorry for the inconvenience.")
        
        else:
            #No errors things works as expected
            print(LOGIC.GETPETNAME(realName))
            return render(request, 'calc/successFirst.html', {'petname':LOGIC.GETPETNAME(realName), 'semNo':LOGIC.GETSEMESTERDETECTION(semesters), 'semlist':LOGIC.GETSEMESTERLIST(semesters)})
            
def choice1(request):
    global semChoice
    if request.method=='POST':
        semChoice = LOGIC.SEMVALTOSEMNAME(str(request.POST["semester"]))
        

        moduleList = semesters[semChoice]

        moduleList.sort(key=lambda x: x.credit, reverse=True)
        
        return render(request, 'calc/successSecond.html', {'semester':semChoice, 'name':realName, 'index':indexNumber, 'modules':moduleList})
    
def choice2(request):

    if request.method=='POST':
        
        #Magule error eka enne nethiwenna...
        moduleList = semesters[semChoice]

        
        LOGIC.ADDINGGRADE(moduleList, request.POST)
        GPA = LOGIC.CALCGPA(moduleList)
        
        return render(request, 'calc/successFinal.html', {'semester':semChoice, 'name':realName, 'index':indexNumber, 'modules':moduleList, 'GPA':GPA})
        


	
