import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os

import csv

import requests
# good to check everythings working with the venv:
if __name__=="__main__":
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is:{sys.executable}\n')



# tomorrow morning its scraping time.
econ_suggested_arrangement=requests.get('https://catalog.utexas.edu/undergraduate/liberal-arts/degrees-and-programs/bachelor-of-arts-plan-i/economics/sugg-eco-ba/')
econsoup=BeautifulSoup(econ_suggested_arrangement.text,'html.parser')

cssuggestedarrangement=requests.get('https://catalog.utexas.edu/undergraduate/natural-sciences/degrees-and-programs/bs-computer-science/sugg-comp-sci-bscompsci/')
cssoup=BeautifulSoup(cssuggestedarrangement.text,'html.parser')

financesuggestedarrangement=requests.get('https://catalog.utexas.edu/undergraduate/business/degrees-and-programs/bachelor-of-business-administration/finance/suggested-arrangement-of-courses/')
financesoup=BeautifulSoup(financesuggestedarrangement.text,'html.parser')

def findcodes(course_soup):
    '''
    Important: this gets ALL course codes in the entire webpage. 
    '''
    course_code_list=[]
    coursecodes=course_soup.find_all('a',attrs={"class": ["bubblelink", "code"]})
    for coursecode in coursecodes:
        coursecode=coursecode.text.replace('\xa0',' ')
        course_code_list.append(coursecode)
    return course_code_list


# first I'll make a 



# print('\nfinding course names\n')
# print(findcodes(course_soup=cssoup))

def find_major_coursedata(course_soup):
    """
    this function returns a dictionary with the key coursename and the values as a list of coursecode and coursehours 
    if there are multiple names of the course it turn into a list of lists for the value. 
    """
    coursecode_nameandhours_dict={}
    # can do multiple find alls hmmm

    # I think I can do all the logic in this function turns out.
    # get only the even and odd trs for sure
    trs=course_soup.find_all('tr',attrs={"class":["even","odd"]})
    
    for row in trs:
        tds=row.find_all('td')
        if len(tds)==3:
            coursename=tds[1]
            minorcertstatus = True
            # make sure it doesnt say minor or certificate
            avoidlist=["minor"]
            for item in avoidlist:
                if item in coursename.get_text().lower():
                    minorcertstatus=False
                    break
            if "major" in coursename.get_text().lower() and minorcertstatus:
                coursename=coursename.get_text().split('(')
        # only keep the first bit of the sentence, the useful info
                coursename=coursename[0].strip()


                firsttd=tds[0]

                # looks for the a's in the current td list
                coursecodes=firsttd.find_all('a',attrs={"class": ["bubblelink", "code"]})
                # print(f'len of coursecodes is {len(coursecodes)}\n')
                for coursecode in coursecodes:
                    coursecode=coursecode.text.replace('\xa0',' ')


                thirdtd=tds[2]
                coursehours='na'
                # gotta compare it to a list, since .get returns a list, since there can be multiple classes
                # .get returns many diferent attributes
                if "hourscol" in thirdtd.get("class",[]):
                    coursehours=thirdtd.get_text()
                coursecode_nameandhours_dict[coursename]=[coursecode, coursehours]

                # the length of the td is 2 when theres no course code
                # this happens when its an unspecified course like upper division course
        elif len(tds)==2:
            coursename=tds[0]
            minorcertstatus = True
            # make sure it doesnt say minor or certificate - only really have to worry about it here with the non specific courses
            avoidlist=["minor","certificate"]
            for item in avoidlist:
                if item in coursename.get_text().lower():
                    minorcertstatus=False
                    break
                

            if "major" in coursename.get_text().lower() and minorcertstatus:
                coursename=coursename.get_text().split('(')
        # only keep the first bit of the sentence, the useful info
                coursename=coursename[0].strip()

                secondtd=tds[1]
                # extra assurance to check the class
                if "hourscol" in secondtd.get("class",[]):
                    coursehours=secondtd.get_text()
                
                # now adding to the dictionary logic
                if coursename not in coursecode_nameandhours_dict:
                    coursecode_nameandhours_dict[coursename]=[['no course code', coursehours]]
                else:
                    coursecode_nameandhours_dict[coursename].append(['no course code',coursehours])

    '''
    In this dictionary I have all the course codes that is in the major. This will be useful for later when
    I need to get the prerequisites as I will only visit the links for the coursecodes.  
    Current problem: not allowing duplicates - Solved by checking if "minor" is in the coursename.
    '''
    return coursecode_nameandhours_dict
# I continue this in the make_majorcourses_csvs.py

def findalldegree_courses(course_soup):
    pass
if __name__=="__main__":
    def getcoursedatabysemester(course_soup):
        # define this one later, just make small tweaks to 
        pass
    # botta bing botta boom hell yeah Im done with ts
    # now for 120 more majors
    def testcases():
        print(f'CS Testing\n')
        csdict=find_major_coursedata(cssoup)

        # turns out theres 8 upper division cs courses
        print(f'Econ Testing\n')

        econdict=find_major_coursedata(econsoup)

        print(f'Finance testing\n')
        financedict=find_major_coursedata(course_soup=financesoup)

    def testcasescall():
        print(testcases())

    print('OLD STUFF NOW\n')



    def scrape_major_course_names(course_soup):
        final_major_course_names=[]
        all_tds=course_soup.find_all('td')

        major_course_names=[td for td in all_tds if "major" in td.get_text().lower()]
        # print(f'major_course_names are{major_course_names}\n')

        for sentence in major_course_names:
            # sentence is now a list since we used .split
            sentence=sentence.get_text().split('(')
            # only keep the first bit of the sentence, the useful info
            sentence=sentence[0]
            final_major_course_names.append(sentence.strip())
        # thats one half, the next is getting the ones with class="courselistcomment"
        # nevermind I think we got all of them since theyre in tds too
        return final_major_course_names


    # show the courses
    print()
    print('scrape_major_course_names')
    print(scrape_major_course_names(course_soup=cssoup))


    def return_raw_major_course_names(course_soup):
        major_course_names=[]
        all_tds=course_soup.find_all('td')

        major_course_names=[td for td in all_tds if "major" in td.get_text().lower()]
        # returns only the tds with "major" in their text
        # this should work to loop over to check class attributes in the matchcode_and_name function
        return major_course_names
    print('return_raw_major_course_names:')
    print(return_raw_major_course_names(course_soup=cssoup))


    def matchcodes_and_names(codelist, rawnamelist):
        code_name_dict={}
        
        for code, name in zip(codelist,rawnamelist):
            # see if they have the class attr
            # the courses without course codes, like "upper division cs course"
            if name.get("class") is None:
                name=name.get_text().split('(')
                # only keep the first bit of the name the useful info
                name=name[0].strip()
                code_name_dict[code]=name
            else: #this is the "upper division x course"
                name=name.get_text().split('(')
                # only keep the first bit of the name the useful info
                name=name[0].strip()
                nocoursecodeplaceholder=""
                code_name_dict[nocoursecodeplaceholder]=name
        return code_name_dict
    # ok next I need to somehow only match the codes that are majors to the list
    # in the find codes function, I can just edit that, so it checks if its a major code or not. 

    # hmmm I could just import them all as tuples or dictionaries and then sort from there, if"major" in the keyword. 

    # I can simply scrape everything, not sort by major at first. I would have to import every line tho and then sort through it looking for the tuples that included major. 
    cscodelist=findcodes(course_soup=cssoup)
    cs_rawnamelist=return_raw_major_course_names(course_soup=cssoup)
    print(f'\nMatchcodes and names is:\n{matchcodes_and_names(codelist=cscodelist,rawnamelist=cs_rawnamelist)}\n')




    def get_prerequisites():
        # I need to get the mufukin prerequisities too
        pass

    # The following is now null, since I was able to scrape from the (major) identifer. 
    def scrape_hardtoget_coursenames(coursesoup, identifier):
        # identifier will be course code like HIS or HDO
        
        pass
