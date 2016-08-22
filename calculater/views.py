from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse

from calculater.models import Feedback
from calculater.models import User
from . import LOGIC
import pickle


#<input type="hidden" name="volposition" value="0">

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


        paths = LOGIC.PickleName()
        if paths==-4:
            #SERVER BUSY
            return render(request, 'calc/signin_busy.html')


        if len(User.objects.all())>60:
            User.objects.all()[0].delete()

        user, created = User.objects.get_or_create(sess_id=request.COOKIES.get('csrftoken'))

        if created:
            user.path = paths
            user.index = indexNumber
            user.save()
        else:
            user.path = paths
            user.index = indexNumber
            user.save()

        #Serializing
        pickle_out = open(paths, 'wb')
        pickle.dump({'realName':realName, 'indexNumber':indexNumber, 'semesters':semesters}, pickle_out)
        pickle_out.close()

        #Handling error situations
        if realName==-2:
            return render(request, 'calc/signin_exception.html')
            
        elif realName==-1:
            return render(request, 'calc/signin_password.html')
        
        elif realName==-3:
            return HttpResponse("This service is no longer exist due to change of moodle structure. Sorry for the inconvenience.")
        
        elif user.index!=indexNumber:
            #You are trying for multiple login at same time
            return render(request, 'calc/signin_multi_login.html') 
        
        else:
            #No errors things works as expected
            return render(request, 'calc/successFirst.html', {'petname':LOGIC.GETPETNAME(realName), 'semNo':LOGIC.GETSEMESTERDETECTION(semesters), 'semlist':LOGIC.GETSEMESTERLIST(semesters)})
    
    else:
        return redirect('/calc/signin/')
            
def choice1(request):
    
    if request.method=='POST':
        
        user = User.objects.get(sess_id=request.COOKIES.get('csrftoken'))

        #OBJ de-serailization
        pickle_in = open(user.path, 'rb')
        data = pickle.load(pickle_in)
        pickle_in.close()

        semChoice = 'BSc Eng. Semester - '+ str(request.POST["semester"])
        data['semChoice'] = semChoice

        #OBJ Serialization
        pickle_out = open(user.path, 'wb')
        pickle.dump(data, pickle_out)
        pickle_out.close()

        #OBJ de-serailization
        pickle_in = open(user.path, 'rb')
        data = pickle.load(pickle_in)
        pickle_in.close()


        moduleList = data['semesters'][data['semChoice']]
        moduleList.sort(key=lambda x: x.credit, reverse=True)

        
    
        return render(request, 'calc/successSecond.html', {'semester':data['semChoice'], 'name':data['realName'], 'index':data['indexNumber'], 'modules':moduleList})
    else:
        return redirect('/calc/signin/')

    
def choice2(request):
    
    if request.method=='POST':
        
        user = User.objects.get(sess_id=request.COOKIES.get('csrftoken'))

        #OBJ de-serailization
        pickle_in = open(user.path, 'rb')
        data = pickle.load(pickle_in)
        pickle_in.close()
        
        data['req'] = request.POST
        
        #OBJ Serialization
        pickle_out = open(user.path, 'wb')
        pickle.dump(data, pickle_out)
        pickle_out.close()
        
        #OBJ de-serailization
        pickle_in = open(user.path, 'rb')
        data = pickle.load(pickle_in)
        pickle_in.close()

        moduleList = data['semesters'][data['semChoice']]
        moduleList.sort(key=lambda x: x.credit, reverse=True)
    
        try:
            LOGIC.ADDINGGRADE(moduleList, data['req'])
        except:
            return render(request, 'calc/signin_multi_login.html') 
            
        GPA = LOGIC.CALCGPA(moduleList)

        return render(request, 'calc/successFinal.html', {'semester':data['semChoice'], 'name':data['realName'], 'index':data['indexNumber'], 'modules':moduleList, 'GPA':GPA, 'post':Feedback.objects.order_by('-date')[:10]})

    else:
        return redirect('/calc/signin/')
    
    
def choice2_post(request):
    if request.method=='POST':
        
        if request.is_ajax():
            
            user = User.objects.get(sess_id=request.COOKIES.get('csrftoken'))
            
            nameGiven = request.POST['name']
            comment = request.POST['message']
            
            #OBJ de-serailization
            pickle_in = open(user.path, 'rb')
            data = pickle.load(pickle_in)
            pickle_in.close()
            
            Feedback.objects.create(name=nameGiven, realName=data['realName'], index=data['indexNumber'], text=comment)
            
            moduleList = data['semesters'][data['semChoice']]
            moduleList.sort(key=lambda x: x.credit, reverse=True)
        
            try:
                LOGIC.ADDINGGRADE(moduleList, data['req'])
            except:
                return render(request, 'calc/signin_multi_login.html') 
        
            GPA = LOGIC.CALCGPA(moduleList)
            
            
            
            return render(request, 'calc/successFinal.html', {'semester':data['semChoice'], 'name':data['realName'], 'index':data['indexNumber'], 'modules':moduleList, 'GPA':GPA, 'post':Feedback.objects.order_by('-date')[:10]})
    
    else:
        return redirect('/calc/signin/')
                

            
        


	
