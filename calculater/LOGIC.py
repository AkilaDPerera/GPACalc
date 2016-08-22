import requests
import re
from bs4 import BeautifulSoup
from time import sleep
import os
import time


class MODULE():
    semester, code, name, credit, gradeEarned = '', '', '', None, None
    
    def __init__(self, semester, code, name, credit):
        self.semester = semester
        self.code = code
        self.name = name
        self.credit = credit
        
    def setGradeEarned(self, grade): #grade = 'A+', 'A ', 'A-'
        self.gradeEarned = grade

class SEMESTER():
    semester, semValue = '', ''
    def __init__(self, semester):
        self.semester = semester
        self.semValue = semester[-1]

#--------------------------------------------------------------------------
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
    indexNumber = (re.findall('1[0-9]{5}[A-Za-z]{1}', str(para[0]))[0])


        
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
                        gpa = float(tds[3].text)
                    except:
                        pass
                    else:
                        semester = tds[0].text[4:]
                        moduleCode = tds[1].text
                        moduleName = tds[2].text
                        
                        module = MODULE(semester, moduleCode, moduleName, gpa)
                        
                        if not(semester in semesters):
                            semesters[semester] = [module]
                        else:
                            semesters[semester].append(module)
            break
    else:
        return -3, 0, 0 #lms web site structure was changed
    
    #Every thing is good to proceed
    return realName, indexNumber, semesters #Semester = {'Bsc. Eng. Semester 1': [module obj, module obj, module obj, ..., module obj]}

#-------------------------------------------------------------------------------------------------------------------------------------

def GETPETNAME(full_name):
    names = sorted(full_name.split(), key=lambda x: len(x), reverse=False)
    for name in names:
        if len(name)>3:
            return name

def GETSEMESTERDETECTION(semesters):
    length = len(semesters)
    if length == 1:
        return 'Only one semester was detected. Please choose it from below and continue'
    else:
        return '%d semesters were detected. Pick your choice and continue.'%(length)


def GETSEMESTERLIST(semesters):
    lst = list(semesters.keys())
    lst.sort()
    return [SEMESTER(element) for element in lst]
    
    
def ADDINGGRADE(moduleList, requestPOST ):
    #Input1 = List of MODULE Objects for each module
    #Input2 = think as a python dict ; {'moduleCode':'A+', 'moduleCode':'A '} likewise
    for module in moduleList:
        data = requestPOST[module.code]
        if data!='Unknown':
            module.setGradeEarned(data)
        elif data=='Unknown':
            module.setGradeEarned('None')

def CALCGPA(moduleList):
    #Input = List of MODULE Objects for each module
    GRADE = {'None':'None', 'A+':4.2, 'A ':4.0, 'A-':3.7, 'B+':3.3, 'B ':3.0, 'B-':2.7, 'C+':2.3, 'C ':2.0, 'C-':1.5, 'D ':1.0, 'F ':0.0}
    
    total = 0
    creditPoints = 0
    
    for module in moduleList:
        value = GRADE[module.gradeEarned]
        
        if value!='None':
            cr = module.credit
            
            total += (value*cr)
            creditPoints += cr

    if total!=0:
        return round(float(total)/creditPoints, 4)
    else:
        return 0

def PickleName():
    for name in ['pickle/data'+str(x)+'.pickle' for x in range(60)]:
        try:
            if (time.time() - os.stat(name).st_mtime)>300: #1 minute only
                return name
        except:
            return name
        else:
            pass
    return -4
    

    
    
    
