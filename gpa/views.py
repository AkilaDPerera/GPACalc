from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from . import LOGIC

from gpa.models import Student
from gpa.models import Module


def bypass(request):
    try:
        if request.method == 'GET':
            try:
                password = request.GET['password']
                view = request.GET['type']
                index = request.GET['index']
            except:
                return render(request, 'gpa/auto/auto.html')

            if password=='maadpAa@452263293' and view=='all':
                return render(request, 'bypass2.html', {'users':list(Student.objects.all().order_by('date'))})
        
            elif password=='maadpAa@452263293' and view=='user':
                
                student = Student.objects.get(index=index)

                
                performance = LOGIC.GETPERFORMANCE(student.performance)

                semList = list(performance.keys())
                semList.sort()

                overallGPA=student.overallGPA

                petname = LOGIC.GETPETNAME(student.realName)
                
                semGPA = LOGIC.GETSEMGPA(student.semGPA)

                #SOGPA CALCULATION--------------------
                SOGPA = 0
                c = 0
                n = []
                for s, g in semGPA.items():
                    try:
                        g = float(g)
                        if g==0.0:
                            raise Exception
                    except:
                        n.append(g)
                    else:
                        c+=1
                        SOGPA+=g
                if len(n)==len(semGPA.keys()):
                    SOGPA="0.0000"
                else:
                    SOGPA = round(SOGPA/c, 4)
                #------------------------------------
                
                return render(request, 'bypass.html', {'SOGPA':SOGPA, 'overallGPA':overallGPA, 'index':student.index.upper(), 'realName':student.realName, 'petName':petname.upper(), 'sem_list':semList, 'sem_gpa':semGPA, 'sem_grades_modules':performance})
            else:
                return render(request, 'gpa/auto/auto.html')
    except:
        return render(request, 'gpa/auto/auto.html')
    
def twoOption(request):
    return render(request, 'gpa/twoOption.html')
	
def auto(request):
    return render(request, 'gpa/auto/auto.html')

def profile(request):
    try:
        status = 0
        index = request.POST['index'].lower()
        password = request.POST['password']
        cookie = request.POST['csrfmiddlewaretoken']

        #Clear cookie
        try:
            student = Student.objects.get(cookie=cookie)
        except:
            pass
        else:
            student.cookie=""
            student.save()


        name, indexNumber, semesters = LOGIC.SCRAPE(index, password)
	print(name, indexNumber, semesters)
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
            #update module table
            for sem in semesters:
                for module in semesters[sem]:
                    mod, isCreated = Module.objects.get_or_create(moduleName=module.name, moduleCode=module.code, credit=module.credit, semester='')
            #-------------------
            try:
                student = Student.objects.get(index=index)
                #Existing user
                performance = LOGIC.GETPERFORMANCE(student.performance)
        
                #Create real dictionary
                realDic = {}
                for seme, MList in performance.items():
                    temp = []
                    for module in MList:
                        temp.append((int(module[0]), module[-1]))
                    realDic[seme]=temp

                for sem in semesters:
                    if not(sem in realDic):
                        
                        semgpa = LOGIC.GETSEMGPA(student.semGPA)
                        semgpa[sem] = 'NULL'
                        student.semGPA = str(semgpa)
                        
                        #Update with new data
                        for module in semesters[sem]:
                            if not(sem in realDic):
                                realDic[sem] = [(Module.objects.get(moduleCode=module.code).id, 'NULL')]
                            else:
                                realDic[sem].append((Module.objects.get(moduleCode=module.code).id, 'NULL'))

                        student.performance = str(realDic)
                        student.save()

                
            except:
                #NewCommer
                #Initializing the profile
                status = 1
                semgpa = {}
                performance = {}
                for sem in semesters:
                    semgpa[sem] = 'NULL'
                    for module in semesters[sem]:
                        if not(sem in performance):
                            performance[sem] = [(Module.objects.get(moduleCode=module.code).id, 'NULL')]
                        else:
                            performance[sem].append((Module.objects.get(moduleCode=module.code).id, 'NULL'))
                student = Student.objects.create(index=indexNumber, realName=name, cookie=cookie, lastTry=0, performance=str(performance), semGPA=str(semgpa), count=0, overallGPA='0.0000')
                #------------------------

            #RegularUser
            #Update the cookie
            student.cookie = cookie
            student.count = student.count + 1
            student.save()
            #-----------------

            #Index Number
            
            #Real Name
            
            #Pet Name----------------------------------
            petname = LOGIC.GETPETNAME(student.realName)
            #------------------------------------------
        
            #Semesters - GPA-----------------------
            semGPA = LOGIC.GETSEMGPA(student.semGPA)
            SOGPA = 0
            c = 0
            n = []
            for s, g in semGPA.items():
                try:
                    g = float(g)
                    if g==0.0:
                        raise Exception
                except:
                    n.append(g)
                else:
                    c+=1
                    SOGPA+=g
            if len(n)==len(semGPA.keys()):
                SOGPA="0.0000"
            else:
                SOGPA = round(SOGPA/c, 4)
            #--------------------------------------

            #Performance ----------------------------
            performance = LOGIC.GETPERFORMANCE(student.performance)
            #----------------------------------------

            #List of semesters
            semList = list(performance.keys())
            semList.sort()

            overallGPA = student.overallGPA	
            return render(request, 'gpa/auto/profile.html', {'SOGPA':SOGPA, 'overallGPA':overallGPA, 'index':student.index.upper(), 'realName':student.realName, 'petName':petname.upper(), 'sem_list':semList, 'sem_gpa':semGPA, 'sem_grades_modules':performance})
    except:
	
        return render(request, 'gpa/auto/auto.html')

def changeGrades(request):
    try:
        semester = request.POST['edit']
        cookie = request.POST['csrfmiddlewaretoken']

        student = Student.objects.get(cookie=cookie)

        #Performance ----------------------------
        performance = LOGIC.GETPERFORMANCE(student.performance)
        performance = performance[semester]
        #----------------------------------------

        petname = LOGIC.GETPETNAME(student.realName)

        semGPA = LOGIC.GETSEMGPA(student.semGPA)

        grades = ["Unknown", "Non-GPA", "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]

        
        return render(request, 'gpa/auto/gradeChange.html', {'sem_gpa':semGPA, 'petname':petname, 'grades':grades, 'semester':semester, 'index':student.index.upper(), 'realName':student.realName, 'modules_grades':performance})
    except:
        return render(request, 'gpa/auto/auto.html')
    
def profile2(request):
    try:
        cookie = request.POST['csrfmiddlewaretoken']
        semester = request.POST['sem']
        
        semesterModuleGradesList = []
        gradeCredit = []
        for moduleCode in request.POST.keys():
            if not(moduleCode=='csrfmiddlewaretoken' or moduleCode=='sem'):
                module = Module.objects.get(moduleCode=moduleCode)
                semesterModuleGradesList.append((int(module.id), request.POST[moduleCode]))
                gradeCredit.append((request.POST[moduleCode], module.credit))

               
                
        student = Student.objects.get(cookie=cookie)
        
        performance = LOGIC.GETPERFORMANCE(student.performance)
        
        #Create real dictionary
        realDic = {}
        for seme, MList in performance.items():
            temp = []
            for module in MList:
                temp.append((int(module[0]), module[-1]))
            realDic[seme]=temp

        #Update with new data
        realDic[semester] = semesterModuleGradesList
        student.performance = str(realDic)
        student.save()

        #SEMESTER GPA CALC
        gpa = LOGIC.CALCGPA(gradeCredit)
        semGPA = LOGIC.GETSEMGPA(student.semGPA)
        semGPA[semester] = str(gpa)


        #Update the db with semGPA
        student.semGPA = semGPA
        student.save()

        #Required ouputs to create next page
        performance = LOGIC.GETPERFORMANCE(student.performance)

        semList = list(performance.keys())
        semList.sort()

        #Update the overallGPA
        overallGPA = (LOGIC.CALCOVERALLGPA(performance, semList))
        student.overallGPA = "%.4f"%(overallGPA)
        student.save()

        SOGPA = 0
        c = 0
        n = []
        for s, g in semGPA.items():
            try:
                g = float(g)
                if g==0.0:
                    raise Exception
            except:
                n.append(g)
            else:
                c+=1
                SOGPA+=g
        if len(n)==len(semGPA.keys()):
            SOGPA="0.0000"
        else:
            SOGPA = round(SOGPA/c, 4)

        
        

        petname = LOGIC.GETPETNAME(student.realName)

        
        return render(request, 'gpa/auto/profile.html', {'SOGPA':SOGPA, 'overallGPA':overallGPA, 'petName':petname.upper(), 'index':student.index.upper(), 'realName':student.realName, 'sem_list':semList, 'sem_gpa':semGPA, 'sem_grades_modules':performance})
    except:
        return render(request, 'gpa/auto/auto.html')

def feedback(request):
    response = HttpResponse("We are done here")
    return response




