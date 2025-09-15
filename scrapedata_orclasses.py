import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os

import csv
import json

# good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is:{sys.executable}\n')


with open('theassetcontainment.json') as assetjson:
    theasset=json.load(assetjson)


# print(len(theasset))

# getting a testlink from the asset
archdata=theasset[0]
schoolname=archdata[list(archdata)[0]]
interiordesignlink=archdata[list(archdata)[1]]

# getting the page
interior_suggested_arrangement=requests.get(interiordesignlink)

# print(f'Interior design link:{interiordesignlink}')

interiorsoup=BeautifulSoup(interior_suggested_arrangement.text,'html.parser')

def getallcourses_splitbysemester(suggcourse_link): 
    '''
    Dictionary of dictionaries, with the keys being semester num , like "1st Semester" and the values being the semester data.  
    Each dictionary in the list of dictionaries will be the coursename as the value and the course code, hours, upper/lower division, and the course type:
    Major, core, minor, or general education.
    Later these categories will be used to create visualizations.

    Also of note is this function does the requests and the beautiful soup stuff INSIDE the function
    '''
    course_suggested_arrangement=requests.get(suggcourse_link)
    course_soup=BeautifulSoup(course_suggested_arrangement.text,'html.parser')
    semesterdictionary={}
    # can do multiple find alls hmmm
    degreename=course_soup.find('h1',attrs={"id":"page-title"}).get_text().strip()
    degreename=degreename.split(',')[-1].replace('\\','-').replace('/','-').strip()
    # I think I can do all the logic in this function turns out.
    # get only the even and odd trs for sure - this gets the semester headings too
    semesterstable=course_soup.select_one('table.sc_courselist')
    unfiltered_trs=course_soup.find_all('tr',attrs={"class":["even","odd"]})

    trs=[]
    # filter to remove orclass tds and add those to trs list
    for tr in unfiltered_trs:
        tds=tr.find_all('td')
        # all keyword checks if all elements are true. In this case, true or false if orclass in each td
        trs.append(tr)
    
    semestercount=0
    # for every grouping of names, code, hours, status
    # this is the BIG FOR LOOP
    currentsemester=''

    for row in trs:
        if  "areaheader" not in row.get("class",[]):
            tds=row.find_all('td')
            if len(tds)==3:
                
                
                coursename=tds[1].get_text().replace('\xa0',' ')
        
                if '(' in coursename and 'or' not in coursename:                    
                    coursename_and_type=coursename.split('(')

                    # print(f'len of course name and type:{len(coursename_and_type)}')
                    # only keep the first bit of the sentence, the useful info
                    coursename=coursename_and_type[0].strip()

                    coursetype=coursename_and_type[-1].split(')')[0]
                    coursetype=f'{coursetype}'

                else:
                    coursename=coursename.strip()

                    coursetype=''
                # now that the coursename is formatted, lets deal with the & stuff


                firsttd=tds[0]
                
                # looks for the a's in the current td list
                coursecodes=firsttd.find_all('a',attrs={"class": ["bubblelink", "code"]})
                # print(f'len of coursecodes is {len(coursecodes)}\n')
                if len(coursecodes)>1:
                    fullcoursecode=''
                    for i in range(len(coursecodes)):
                        if i==len(coursecodes)-1:
                            fullcoursecode+=coursecodes[i].text.replace('\xa0',' ')
                        else:
                            fullcoursecode+=f'{coursecodes[i].text.replace('\xa0',' ')} & '


                    coursecode=fullcoursecode.replace('\xa0',' ')

                else:
                    for onecoursecode in coursecodes:
                        # defines coursecode here although tricky. Remove Unicode space.
                        # coursecode is essentially just a string here
                        coursecode=onecoursecode.text.replace('\xa0',' ')

                if "PHL 329" in coursecode:
                        print(f'coursecode {coursecode}\n\n\n')

# -----------------------------------------------------------------------------------------------
                # now that the unicode code is out, look for the & and replace them
                # have to use the original html tag not the text
                nameblock=tds[1].find('span',class_="blockindent")
                codeblock=tds[0].find('span',class_="blockindent")

                originalcoursecode=coursecode


                if nameblock:   
                    coursename=coursename.split('and')

                    fullname=''
                    for i in range(len(coursename)):
                        if i==len(coursename)-1:
                            fullname+=coursename[i].strip()

                        else:
                            fullname+=coursename[i].strip()+' and '
                    # reassign
                    coursename=fullname
                    
                
                    # end dealing with 'and' stuff
                
                    

                

                # turns out coursecode is a string

                # get the status from the number stuff

                lowerdivstatus="Lower Division"
                upperdivstatus="Upper Division"
                status=''
                # check if theres a number in it then move onto the logic
                if not codeblock:
                    if any(char.isdigit() for char in coursecode):
                        coursenum=coursecode.split(' ')[-1][1:3]
                        if int(coursenum)>=20:
                            status=upperdivstatus
                        else:
                            status=lowerdivstatus
                elif codeblock:
                    firstcourse=coursecode.split('&')[0].strip()
                    if any(char.isdigit() for char in firstcourse):
                            coursenum=coursecode.split(' ')[-1][1:3]
                            if int(coursenum)>=20:
                                status=upperdivstatus
                            else:
                                status=lowerdivstatus
              

                

                thirdtd=tds[2]
                coursehours='na'
                # gotta compare it to a list, since .get returns a list, since there can be multiple classes

                # .get returns many diferent attributes - very useful
                if "hourscol" in thirdtd.get("class",[]):
                    coursehours=thirdtd.get_text()

                # making the dictionary of dictionaries logic here
              
                semesterdictionary[currentsemester][coursename]=[coursecode, coursehours, status, coursetype]

                # get and add the upper and lower division stuff
                

                # the length of the td is 2 when theres no course code
                # this happens when its an unspecified course like upper division course
            elif len(tds)==2:
                '''or class tr length is always 2.
                I think all or classes have coursecodes too
                '''

                if "orclass" in tds[0].get("class", []):
                    # print(f'orclass {tds[0].get_text()}')
                    coursename = tds[1]
                    coursecode = tds[0].get_text().replace('\xa0',' ')
                    if "PHL 329" in coursecode:
                        print(f'coursecode {coursecode}\n\n\n')

                # print(f'Coursename {coursename.get_text()}')
                    if '(' in coursename.get_text().lower() and 'or' not in coursename.get_text().lower():

                
                        coursename=coursename.get_text()
                        coursename_and_type=coursename.split('(')

                        # only keep the first bit of the sentence, the useful info
                        coursename=coursename_and_type[0].strip()
                        coursetype=coursename_and_type[1].split(')')[0]
                        coursetype=f'{coursetype}'
                    else:
                        coursename=coursename.get_text().strip()
                        coursetype=''
                    
                    # print(f'Coursename {coursename}')





                    # getting and assigning the status variable
                    lowerdivstatus="Lower Division"
                    upperdivstatus="Upper Division"
                    status=''

                    if "lower" in coursename.lower():
                        status=lowerdivstatus
                    elif "upper" in coursename.lower():
                        status=upperdivstatus
                    else:
                        # if neither upper or lower leave it blank. Remember these are the lines with no course code
                        status=''

                    secondtd=tds[1]

                    manuallist=['PHL 329','UTS 360','UTS 355']
                    # extra assurance to check the class
                    if "hourscol" in secondtd.get("class",[]):
                        coursehours=secondtd.get_text()
                    
                    # now adding to the dictionary logic
                    
                    # this was certainly a thought experiment mf
                
                    # this is for multiple of one class in one semester. LIke "upper div elective"
                    # however when theres multiple they usually never have a coursecode.
                    if coursename not in semesterdictionary[currentsemester]:
                        semesterdictionary[currentsemester][coursename]=[[coursecode, coursehours, status, coursetype]]
                    else:
                        if any(item in coursecode for item in manuallist):

                            coursename+='removemelater'
                            # print(f'Coursename we are appending{semesterdictionary[currentsemester][coursename]}]')
                            semesterdictionary[currentsemester][coursename]=[[coursecode,coursehours,status, coursetype]]

                        else:
                            semesterdictionary[currentsemester][coursename].append([coursecode,coursehours,status, coursetype])

                        # get upper div by textin coursename for this one since no coursecode
                elif "orclass" not in tds[0].get("class", []):
                    coursename = tds[0]
                    coursecode = tds[1]

                    if '(' in coursename.get_text().lower() and 'or' not in coursename.get_text().lower():

            
                        coursename=coursename.get_text()
                        coursename_and_type=coursename.split('(')

                        # only keep the first bit of the sentence, the useful info
                        coursename=coursename_and_type[0].strip()
                        coursetype=coursename_and_type[1].split(')')[0]
                        coursetype=f'{coursetype}'
                    else:
                        coursename=coursename.get_text().strip()
                        coursetype=''
                    
                    # print(f'Coursename {coursename}')





                        # getting and assigning the status variable
                    lowerdivstatus="Lower Division"
                    upperdivstatus="Upper Division"
                    status=''

                    if "lower" in coursename.lower():
                        status=lowerdivstatus
                    elif "upper" in coursename.lower():
                        status=upperdivstatus
                    else:
                        # if neither upper or lower leave it blank. Remember these are the lines with no course code
                        status=''

                    secondtd=tds[1]


                    # extra assurance to check the class
                    if "hourscol" in secondtd.get("class",[]):
                        coursehours=secondtd.get_text()
                    
                    # now adding to the dictionary logic
                    
                    # this was certainly a thought experiment mf
                
                    # this is for multiple of one class in one semester. LIke "upper div elective"
                    # however when theres multiple they usually never have a coursecode.
                    if coursename not in semesterdictionary[currentsemester]:
                        semesterdictionary[currentsemester][coursename]=[['', coursehours, status, coursetype]]
                    else:
                        semesterdictionary[currentsemester][coursename].append(['',coursehours,status, coursetype])

                    # get upper div by textin coursename for this one since no coursecode

                
                
        # areaheader is the semester classes
        elif  "areaheader" in row.get("class",[]):
            semestercount+=1

            semesterorder=row.select_one('span.courselistcomment.areaheader').get_text() 
            currentsemester=semesterorder
            # establish each semester dictionary
            semesterdictionary[currentsemester]={}

    # this shows up in makedatafiles.py but its ok
    print(f'Created semesterdictionary for {degreename}')
    return semesterdictionary


if __name__=="__main__":
    print('Calling getallcourses_splitbysemester')
   
    print('Economics:')
    testlink='https://catalog.utexas.edu/undergraduate/geosciences/degrees-and-programs/bs-geological-sciences/sugg-geo-sci-bsgeosci/'
    testdict=getallcourses_splitbysemester(suggcourse_link=testlink)
    for currentsemester in testdict.values():
        for key,value in currentsemester.items():
            if isinstance(value, list):
                print(value)




