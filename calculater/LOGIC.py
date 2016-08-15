def SCRAPE(username, password):
    import requests
    from bs4 import BeautifulSoup
    import re
    
    c= requests.Session()
    
    url = 'https://lms.mrt.ac.lk/login.php'
    
    loginData = {'LearnOrgUsername': username,
                 'LearnOrgPassword': password, 'LearnOrgLogin': 'Login'}
    
    c.get(url)
    
    c.post(url, data=loginData)
    
    data = c.get("https://lms.mrt.ac.lk/enrolments.php")

#----------
    nameIndex = []
    if data.url=="https://lms.mrt.ac.lk/enrolments.php":
        #Get the web page properly
        soups = BeautifulSoup(data.content)
        
        #Getting name and Index
        para = soups('p')
        nameIndex.append((re.findall('([A-Z ]+)</p>$', str(para[0]))[0]).title())
        nameIndex.append((re.findall('1[0-9]{5}[A-Za-z]{1}', str(para[0]))[0]))
        
    
        
        tables = soups('table')
        #Finding the specific table
        for table in tables:
            if (table.get('cellspacing', None)=='1') and (table.get('cellpadding', None)=='1') and (table.get('class', None)==['bodytext']):
                #Got the table
                trows = table('tr')
                
                #We get all the rows of data as list in trows
                
                GPASUM = 0
                scrapedSum = 0
                current_semester = ''
                module = []
                
                index = -1
                for tr in trows[::-1]:
                    index += 1
                    
                    tds = tr('td')
                    if len(tds)==4:
                        if current_semester=='': 
                            current_semester = tds[0].text
                            scrapedSum = float(trows[::-1][index-1]('td')[1].text)
                                                    
                        if current_semester==tds[0].text:
                            GPASUM +=  float(tds[3].text)
                            module.append([tds[1].text, tds[2].text, float(tds[3].text)])
                            
                        else:
                            break
                        
                break
        else:
            #No such table found
            return -1,0,0,0
        
        #Contradiction with calc GPA with scraped GPA
        if scrapedSum==GPASUM:
            return (nameIndex, current_semester, GPASUM, module)
        else:
            return -1,0,0,0
    else:
        #Did get the web page properly
        return -2,0,0,0#Incorrect password
            
#-----------


class MODULE():
    code = ''
    name = ''
    GPAcredit, gradeEarned = None, None
    
    def __init__(self, module):
        self.code = module[0]
        self.name = module[1]
        self.GPAcredit = module[2]
    def setGradeEarned(self, value):
        self.gradeEarned = value

def ModuleToObject(modules):
    lst = []
    for module in modules:
        lst.append(MODULE(module))
    return lst

def ConnectPost(modules, POST):
    for module in modules:
        data = POST[module.code]
        if data!='Unkwown':
            module.setGradeEarned(data)
        elif data=='Unkwown':
            module.setGradeEarned('None')

def CalcGPA(modules):
    GRADE = {'None':'None', 'A+':4.2, 'A ':4.0, 'A-':3.7, 'B+':3.3, 'B ':3.0, 'B-':2.7, 'C+':2.3, 'C ':2.0, 'C-':1.5, 'D ':1.0, 'F ':0.0}
    total = 0
    credit = 0
    for module in modules:
        data = GRADE[module.gradeEarned]
        
        if data!='None':
            cr = module.GPAcredit
            total += (data*cr)
            credit += cr
    if total!=0:
        return float(total)/credit
    else:
        return 0
    
    

    
    
    
