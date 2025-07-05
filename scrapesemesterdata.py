import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os

import csv

# good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is:{sys.executable}\n')


from theassetcontainment import theasset


# print(len(theasset))

# getting a testlink from the asset
archdata=theasset[0]
schoolname=archdata[list(archdata)[0]]
interiordesignlink=archdata[list(archdata)[1]]

# getting the page
interior_suggested_arrangement=requests.get(interiordesignlink)
interiorsoup=BeautifulSoup(interior_suggested_arrangement.text,'html.parser')

def getallcourses_splitbysemester(suggcourse_link): 
    '''
    Returns a list of dictionaries. In each dictionary, the first key will be Semester and the first value will be the number of the semester.
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
    degreename=degreename.split(',')[-1].replace('\\','-')
    # I think I can do all the logic in this function turns out.
    # get only the even and odd trs for sure - this gets the semester headings too
    unfiltered_trs=course_soup.find_all('tr',attrs={"class":["even","odd"]})

    trs=[]
    # filter to remove orclass tds and add those to trs list. This is kinda complex.
    for tr in unfiltered_trs:
        tds=tr.find_all('td')
        # all keyword checks if all elements are true. In this case, true or false if orclass in each td
        if all("orclass" not in td.get("class", []) for td in tds):
            trs.append(tr)
    
    semestercount=0
    # for every grouping of names, code, hours, status
    # this is the BIG FOR LOOP
    for row in trs:
        if  "areaheader" not in row.get("class",[]):
            tds=row.find_all('td')
            if len(tds)==3:

                coursename=tds[1]
            
                coursename_and_type=coursename.get_text().split('(')
        # only keep the first bit of the sentence, the useful info
                coursename=coursename_and_type[0].strip()

                coursetype=coursename_and_type[1].split(')')[0]

                firsttd=tds[0]

                # looks for the a's in the current td list
                coursecodes=firsttd.find_all('a',attrs={"class": ["bubblelink", "code"]})
                # print(f'len of coursecodes is {len(coursecodes)}\n')
                for coursecode in coursecodes:
                    # defines coursecode here although tricky. Remove Unicode space.
                    coursecode=coursecode.text.replace('\xa0',' ')

                

                # turns out coursecode is a string

                # get the status from the number stuff

                lowerdivstatus="Lower Division"
                upperdivstatus="Upper Division"
                status=''
                # check if theres a number in it
                if any(char.isdigit() for char in coursecode):
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
                semesterdictionary[coursename]=[coursecode, coursehours, status, f'({coursetype})']

                # get and add the upper and lower division stuff
                

                # the length of the td is 2 when theres no course code
                # this happens when its an unspecified course like upper division course
            elif len(tds)==2:


                coursename=tds[0]

                        
                            
                coursename_and_type=coursename.get_text().split('(')
                # only keep the first bit of the sentence, the useful info
                coursename=coursename_and_type[0].strip()
                coursetype=coursename_and_type[1].split(')')[0]




                # getting and assigning the status variable
                lowerdivstatus="Lower Division"
                upperdivstatus="Upper Division"
                status=''
                if "lower" in coursename.lower():
                    status=lowerdivstatus
                elif "upper" in coursename.lower():
                    status=upperdivstatus
                else:
                    # if neither upper or lower leave it blank
                    status=''

                secondtd=tds[1]


                # extra assurance to check the class
                if "hourscol" in secondtd.get("class",[]):
                    coursehours=secondtd.get_text()
                
                # now adding to the dictionary logic
                if coursename not in semesterdictionary:
                    # removed it from "no course code" to just an empty string
                    semesterdictionary[coursename]=[['', coursehours,status, f'({coursetype})']]
                else:
                    semesterdictionary[coursename].append(['',coursehours,status, f'({coursetype})'])

                    # get upper div by textin coursename for this one since no coursecode
                

        elif  "areaheader" in row.get("class",[]):
            semestercount+=1
            print('\n there was an areaheader\n')

            semesternum=row.find('span',{"class":["courselistcomment","areaheader"]}).get_text()
            semesterdictionary[f'Semester {semestercount}']=semesternum
            
    print(f'Created semesterdictionary for{degreename}\n')
    return semesterdictionary

def splitupsemesters(course_soup):
    pass
# the semester headings have the "areaheader" class. Use this to our advantage later.

if __name__=="__main__":
    print('Calling getallcourses_splitbysemester')
    getallcourses_splitbysemester(suggcourse_link=interiordesignlink)
    print('\nThe following should be the semesterdictionary output\n')
    print(getallcourses_splitbysemester(suggcourse_link=interiordesignlink))