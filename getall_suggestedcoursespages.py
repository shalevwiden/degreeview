import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os
import webbrowser
import time

# csvs should be light to create with every single course I'm not gonna lie
# and then even colorful excelfiles too ngl

import csv

import requests

# then I'll need to import my find_major_coursedata function too
# good to check everythings working with the venv:

'''
Essentially, this entire file is for the creation of theasset later in the page
'''

if __name__=='__main__':

    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is:{sys.executable}\n')

# make a dictionary with the major name and the suggested courses link

def getbasecollegelinks():
    baseurl=requests.get('https://catalog.utexas.edu/undergraduate/')
    undergradcatalog_soup=BeautifulSoup(baseurl.text, 'html.parser')

    # this is where all the links to the college pages are
    contentarea=undergradcatalog_soup.find('div', attrs={"class":"sitemap"})

    collegelinks=[a['href'] for a in contentarea.find_all('a') if "school" in a.text.lower() or "college" in a.text.lower()]
    print(type(collegelinks))
    colleges=[a.get_text() for a in contentarea.find_all('a') if "school" in a.text.lower() or "college" in a.text.lower()]
    # colleges is a list of colleges and schools at UT not their links tho
    return collegelinks

def getcollegenames():
    baseurl=requests.get('https://catalog.utexas.edu/undergraduate/')
    undergradcatalog_soup=BeautifulSoup(baseurl.text, 'html.parser')

    # this is where all the links to the college pages are
    contentarea=undergradcatalog_soup.find('div', attrs={"class":"sitemap"})

    colleges=[a.get_text() for a in contentarea.find_all('a') if "school" in a.text.lower() or "college" in a.text.lower()]
    # colleges is a list of colleges and schools at UT not their links tho

    colleges=colleges[1:-1]
    return colleges


def make_fullcollege_urls(collegelinks):
    firsthalfofurl="https://catalog.utexas.edu"
    fullurls=[]
    lasthalfofurl='degrees-and-programs/'
    # remove the first and last
    onlycollegelinks=collegelinks[1:-1]

    for link in onlycollegelinks:
        fullurl=f'{firsthalfofurl}{link}{lasthalfofurl}'
        fullurls.append(fullurl)
    
    return fullurls


def test_full_urls(fullurls):
    for url in fullurls:
        webbrowser.open_new_tab(url)
        time.sleep(1)
# test_full_urls(make_full_urls(collegelinks=collegelinks))

# one college page as a time, and then can loop over this, easy peasy
def getsuggcoursespages(degreeandprogramurl):
    '''
    parameter url should be the url for the school degrees and programs page, returned by the:
    by the "make_fullcollege_urls() function
    '''
    degreespage=requests.get(degreeandprogramurl)
    degreesoup=BeautifulSoup(degreespage.text,'html.parser')

    # this self class worked as it was the only li to have self it turned out

    majornav=degreesoup.find('li', attrs={"class":"self"})
    # I'm checking the text, not the url, so I should be fine with sugg or even suggested
    majorslinks=[a['href'] for a in majornav.find_all('a') if "sugg" in a.get_text().lower()]
    full_majorlinks=[]

    for link in majorslinks:
        firsthalf='https://catalog.utexas.edu'
        fulllink=f'{firsthalf}{link}'

        full_majorlinks.append(fulllink)

    # print(len(majornav))
    return full_majorlinks


def make_suggcoursepage_and_degreename_dict(fullmajorlinks):
    sugglink_and_degreename_dict={}

    # first add the schoolname as the first element in the dictionary
    schoollink=fullmajorlinks[-1]
    schoollink=schoollink.split('/')
    reconstructedlink=f'{schoollink[0]}//{schoollink[2]}/{schoollink[3]}/{schoollink[4]}/'
    print(f'reconstructedlink is {reconstructedlink}')

    schoolspage=requests.get(reconstructedlink)
    schoolsoup=BeautifulSoup(schoolspage.text,'html.parser')
    schoolname=schoolsoup.find("h1",attrs={"id":"page-title"}).get_text().strip()
    
    # school name as first element
    sugglink_and_degreename_dict['School_Name']=schoolname

    for link in fullmajorlinks:
        suggcourselink=requests.get(link)
        suggcoursesoup=BeautifulSoup(suggcourselink.text,'html.parser')
        degreename=suggcoursesoup.find("h1",attrs={"id":"page-title"}).get_text().strip()
        # change this to allow for degrees with more commas
        if degreename.count(',')==1: 
            # .count works for list and strings great
            degreename=degreename.split(',')[-1].strip()
        else:
            suggheading,restofdegreename=degreename.split(',')[0], degreename.split(',')[1:]
            degreename=''
            for i in range(len(restofdegreename)):
                if i==len(restofdegreename)-1:
                    degreename+=f' {restofdegreename[i].strip()}'
                else:
                    degreename+=f'{restofdegreename[i].strip()},'
            degreename=degreename.strip()

        # this line right here, this is the magic 
        sugglink_and_degreename_dict[degreename]=link
    
    # add school name as the last item in the dict.
    
    return sugglink_and_degreename_dict






def makelistofdicts(alldegreesandprogramsurls):
    # what it takes in is a list of all degrees and programs urls
    full=len(alldegreesandprogramsurls)
    amountwegonnado=5
    dolist=[]
    for i in range(full):
        dolist.append(alldegreesandprogramsurls[i])
        # this shows up in testing when I create the asset by calling the function
        print(alldegreesandprogramsurls[i])

    
    listofdicts=[]


    for schoolpagelink in dolist:
        suggcourses=getsuggcoursespages(schoolpagelink)
        # if the suggested course list has something in it
        if suggcourses:
            schooldict=make_suggcoursepage_and_degreename_dict(suggcourses)
            listofdicts.append(schooldict)
        else:
            # this helped me realize pharmacy has none and was throwing off the code
            print(f'\nThere were no sugg courses for {schoolpagelink}\n')

    return listofdicts


        
     
    
    



    # I could use this one. Actually I will if I get more than one
    # for li in degreesoup.select(".item.special.highlighted"):
        # print("✔ Found via CSS:", div)

if __name__=='__main__':
    print(f'\ngetbasecollegelinks() is {getbasecollegelinks()}\n')
    collegelinks=getbasecollegelinks()
    allcollegedegreesandprogramsurls=make_fullcollege_urls(collegelinks=collegelinks)
    print('\nalldegrees and programs urls:\n\n')
    print(allcollegedegreesandprogramsurls)

    print('Full URLs: \n')
    print(make_fullcollege_urls(collegelinks=collegelinks))

    # enter the following into the function below:
    allcollegedegreesandprogramsurls=make_fullcollege_urls(collegelinks=collegelinks)
    print('What I\'m enterin into the func:\n')
    print(allcollegedegreesandprogramsurls)

    print('but this doesnt works?\n')
    print('Full URLs: \n')
    print(make_fullcollege_urls(collegelinks=collegelinks))
    print('\nFinding sugg courses URLS:\n')

    full_major_links=getsuggcoursespages('https://catalog.utexas.edu/undergraduate/architecture/degrees-and-programs/')
    print(f'\n\nFull major links:\n\n{full_major_links}')

    completeddict=make_suggcoursepage_and_degreename_dict(fullmajorlinks=full_major_links)
    print('\nCompleted dict:\n')
    print(completeddict)

    print('\n\n\n\n\n\n')
    print('List of Dicts:\n')

    activate_theasset=True

    if activate_theasset:
        #  -- the asset --
        theasset=makelistofdicts(alldegreesandprogramsurls=allcollegedegreesandprogramsurls)

        print('\nThe asset:\n')
        print(theasset)


    print('\n\n')


def getmajorsnames():
    pass

# this is just like a slow crawl to get all of the suggested links but we can do it for sure lol. 


