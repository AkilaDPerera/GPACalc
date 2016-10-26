from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from . import LOGIC

from gpa.models import Student
from gpa.models import Module



def twoOption(request):
    return render(request, 'gpa/twoOption.html')
	
def auto(request):
    return render(request, 'gpa/auto/auto.html')

def profile(request):
    status = 0
    index = request.POST['index'].lower()
    password = request.POST['password']
    cookie = request.POST['csrfmiddlewaretoken']

    #index = "140457t"
    #password = "maadpAa@452263293"

    name, indexNumber, semesters = LOGIC.SCRAPE(index, password)

    if name==-1:
        pass
    elif name==-2:
        pass
    elif name==-3:
        pass
    else:
        #update module table
        for sem in semesters:
            for module in semesters[sem]:
                mod, isCreated = Module.objects.get_or_create(moduleName=module.name, moduleCode=module.code, credit=module.credit, semester=module.semester)
        #-------------------
        try:
            student = Student.objects.get(index=index)
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
            student = Student.objects.create(index=indexNumber, realName=name, cookie=cookie, lastTry=0, performance=str(performance), semGPA=str(semgpa), count=0, overallGPA=0.0)
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
        #--------------------------------------

        #Performance ----------------------------
        performance = LOGIC.GETPERFORMANCE(student.performance)
        #----------------------------------------

        #List of semesters
        semList = list(performance.keys())
        semList.sort()

        overallGPA = student.overallGPA

        return render(request, 'gpa/auto/profile.html', {'overallGPA':overallGPA, 'index':student.index, 'realName':student.realName, 'petName':petname, 'sem_list':semList, 'sem_gpa':semGPA, 'sem_grades_modules':performance})


def changeGrades(request):
    semester = request.POST['edit']
    cookie = request.POST['csrfmiddlewaretoken']

    student = Student.objects.get(cookie=cookie)

    #Performance ----------------------------
    performance = LOGIC.GETPERFORMANCE(student.performance)
    performance = performance[semester]
    #----------------------------------------

    grades = ["Unknown", "Non-GPA", "A+", "A", "A-", "B+", "B", "B-", "C+", "C", "C-", "D", "F"]

    
    return render(request, 'gpa/auto/gradeChange.html', {'grades':grades, 'semester':semester, 'index':student.index, 'realName':student.realName, 'modules_grades':performance})

def profile2(request):
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
    student.overallGPA = overallGPA
    student.save()

    
    

    petname = LOGIC.GETPETNAME(student.realName)

    
    return render(request, 'gpa/auto/profile.html', {'overallGPA':overallGPA, 'petName':petname, 'index':student.index, 'realName':student.realName, 'sem_list':semList, 'sem_gpa':semGPA, 'sem_grades_modules':performance})
