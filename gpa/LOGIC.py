import requests
import re
from bs4 import BeautifulSoup
from time import sleep
import os
import time

from django.contrib.auth.models import User
from gpa.models import Profile
from gpa.models import Semester
from gpa.models import Performance
from gpa.models import Module


from django.template.defaulttags import register

@register.filter
def get_item(dictionary, key):
    return dictionary.get(key) 

class MODULE():
    def __init__(self, code, name, credits):
        self.code = code
        self.name = name
        self.credits = credits
        
    def getModuleCode(self):
        return self.code
    
    def getModuleName(self):
        return self.name
    
    def getModuleCredits(self):
        return self.credits
    
    def __str__(self):
        return self.code + " : " + self.name
    
    def __repr__(self):
        return self.code + " : " + self.name

def SCRAPE(username, password):
    """
    ERROR RETURNS,
    -1 : incorrect passward 
    -2 : Exception occurs at login in both two tries
    -3 : lms web site structure was changed
    """
    for trytologin in range(2):
        try:
            c= requests.Session()
    
            url = 'https://lms.mrt.ac.lk/login.php'
    
            loginData = {'LearnOrgUsername': username,
                 'LearnOrgPassword': password, 'LearnOrgLogin': 'Login'}
    
            c.get(url)
    
            c.post(url, data=loginData)
    
            data = c.get("https://lms.mrt.ac.lk/enrolments.php")
            
        except:
            sleep(3)
        
        else:
            break
    else:
        return -2, 0, 0 #Exception occurs at login in both two tries
    
    #No exception at login
    
    if data.url!="https://lms.mrt.ac.lk/enrolments.php": #If passward incorrect
        return -1, 0, 0
    
    #Login to moodle sucessful we have the web content required 'data'

    soups = BeautifulSoup(data.content)
        
    #Getting name and Index
    para = soups('p')
    realName = (re.findall('([A-Z ]+)</p>$', str(para[0]))[0]).title()
    indexNumber = (re.findall('1[0-9]{5}[A-Za-z]{1}', str(para[0]))[0]).lower()


        
    tables = soups('table')
    #Finding the specific table
    for table in tables:
        if (table.get('cellspacing', None)=='1') and (table.get('cellpadding', None)=='1') and (table.get('class', None)==['bodytext']):
            #Got the table
            trows = table('tr')
                
            #We get all the rows of data as list in trows
            semesters = {}
            
            currentIndex = -1
            for tr in trows[::-1]:
                currentIndex += 1
    
                tds = tr('td')

                if len(tds)==4:#Possible data set
                    try:
                        credits = float(tds[3].text.strip())
                    except:
                        pass
                    else:
                        semester = tds[0].text[4:].strip()
                        moduleCode = tds[1].text.strip()
                        moduleName = tds[2].text.strip()
                        
                        module = MODULE(moduleCode, moduleName, credits)
                        
                        if not(semester in semesters):
                            semesters[semester] = [module]
                        else:
                            semesters[semester].append(module)
            break
    else:
        return -3, 0, 0 #lms web site structure was changed

    if (realName=='' or semesters==''):
        return -3, 0, 0
    
    #Every thing is good to proceed
    return realName, indexNumber, semesters #Semester = {'Bsc. Eng. Semester 1': [module obj, module obj, module obj, ..., module obj]}



def GETPETNAME(full_name):
    ls = full_name.split()
    ls.sort()
    names = sorted(ls, key=lambda x: len(x), reverse=False)
    for name in names:
        if len(name)>3:
            return name

def GETPERFORMANCE(data):
    performance = dict()
    for semester in sorted(list(set(data.values_list("semester")))):
        sem = Semester.objects.get(id=semester[0])
        for entry in data.filter(semester=sem):
            if sem not in performance.keys():
                performance[sem] = [entry]
            else:
                performance[sem].append(entry)
        performance[sem] = sorted(performance[sem], key=lambda x: x.module.credit, reverse=True)
    return performance
    
def GETGPAS(performance):
    GRADE = {'A+':4.2, 'A':4.0, 'A-':3.7, 'B+':3.3, 'B':3.0, 'B-':2.7, 'C+':2.3, 'C':2.0, 'C-':1.5, 'D':1.0, 'F':0.0}
    semGPA = dict()
    sem_list = []
    wholeCredits = 0.0
    wholeCreditsXGrade = 0.0
    totOfSemGPA = 0.0
    noOfSems = 0
    
    for sem in performance.keys():
        totalCredits = 0.0
        creditsXgrade = 0.0
        
        for module in performance[sem]:
            if (module.grade!="UNKNOWN" and module.grade!="Non-GPA"):
                totalCredits += float(module.module.credit)
                creditsXgrade += GRADE[module.grade] * float(module.module.credit)
        if totalCredits!=0.0:
            semGPA[sem] = round(creditsXgrade/totalCredits, 2)
            totOfSemGPA += (creditsXgrade/totalCredits)
            noOfSems += 1
        else:
            semGPA[sem] = "NOT-INITIALIZED"
        
        #Getting overall GPA
        wholeCredits += totalCredits
        wholeCreditsXGrade += creditsXgrade
        sem_list.append(sem)
    
    if (wholeCredits!=0.0):
        overallGPABestMethod = round(wholeCreditsXGrade/wholeCredits, 4)
        overallGPACorrecMethod = round(totOfSemGPA/noOfSems, 4)
        return semGPA, "%.4f"%(overallGPABestMethod), "%.4f"%(overallGPACorrecMethod), sorted(sem_list, key=lambda x: x.semesterName, reverse=False)
    else:
        return semGPA, "%.4f"%(0.0), "%.4f"%(0.0), sorted(sem_list, key=lambda x: x.semesterName, reverse=False)

def GETCLASS(correctGPA):
    correctGPA = float(correctGPA)
    if correctGPA>=4.0:
        return 1, "First Class"
    elif correctGPA>=3.7:
        return 2, "First Class"
    elif correctGPA>=3.3:
        return 3, "Second Upper"
    elif correctGPA>=3.0:
        return 4, "Second Lower"
    elif correctGPA>=2.0:
        return 5, "General"
    else:
        return 6, "----"


























        
        
##
##class SEMESTER():
##    semester, semValue = '', ''
##    def __init__(self, semester):
##        self.semester = semester
##        self.semValue = semester[-1]
##
###--------------------------------------------------------------------------
##
###-------------------------------------------------------------------------------------------------------------------------------------
##
##
##def GETSEMESTERLIST(semesters):
##    lst = list(semesters.keys())
##    lst.sort()
##    return [SEMESTER(element) for element in lst]
##    
##    
##def ADDINGGRADE(moduleList, requestPOST ):
##    #Input1 = List of MODULE Objects for each module
##    #Input2 = think as a python dict ; {'moduleCode':'A+', 'moduleCode':'A '} likewise
##    for module in moduleList:
##        data = requestPOST[module.code]
##        if data!='Unknown':
##            module.setGradeEarned(data)
##        elif data=='Unknown':
##            module.setGradeEarned('None')
##
##
##def PickleName():
##    for name in ['pickle/data'+str(x)+'.pickle' for x in range(60)]:
##        try:
##            if (time.time() - os.stat(name).st_mtime)>300: #1 minute only
##                return name
##        except:
##            return name
##        else:
##            pass
##    return -4
##    

    
    
    
