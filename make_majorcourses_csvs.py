import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os

import csv

import requests
# good to check everythings working with the venv:
print(f'the version of beautiful soup is\n {(bs4.__version__)}')
print(f'the version of requests is\n {(requests.__version__)}')
print(f'\nthe python version being used is:{sys.executable}\n')

from coursescraping import find_major_coursedata
from theassetcontainment import theasset

# first I'll make the CSV's then I can easily modify it to go into an excel file from there. 

archdata=theasset[0]

def makelistof_majordata_dicts(schooldata):
    # schooldata is every dict thats in theasset
    """
    This returns a list of dictionaries where each dictionary has a dictionary as its value and the degree name as the Key

    In addition the dictionary that is the value is a dictionary of lists.
    kinda complicated...
    """
    schoolname=schooldata[list(schooldata)[0]]
    schooldir=schoolname

    list_ofmajordata_dicts=[]
    # for every element in the school wide dictionary. Not [0] cause thats the school name
    
    for i in range(1,len(schooldata)):
            key=list(schooldata)[i]
            degreename=key

            sugglink=schooldata[key]

            sugg_request=requests.get(sugglink)
            degreesoup=BeautifulSoup(sugg_request.text,"html.parser")

            degreename_major_coursedatadict={}
            major_coursedata=find_major_coursedata(course_soup=degreesoup)

            degreename_major_coursedatadict[degreename]=major_coursedata

            list_ofmajordata_dicts.append(degreename_major_coursedatadict)

    return list_ofmajordata_dicts
print('testing:\n')
print('test the find_major_coursedata function again')


cssuggestedarrangement=requests.get('https://catalog.utexas.edu/undergraduate/natural-sciences/degrees-and-programs/bs-computer-science/sugg-comp-sci-bscompsci/')
cssoup=BeautifulSoup(cssuggestedarrangement.text,'html.parser')
print(find_major_coursedata(course_soup=cssoup))
print('\nmakelistof_majordata_dicts\n')

biglist=makelistof_majordata_dicts(archdata)
for i in biglist:
    print(f'\n{i}\n')



def make_majorcoursesonly_csvs(schooldata):
    '''
    this function doesnt take a list of major data dicts returned by the function above.
    But does call it. It has to take the schooldata dict so it can be placed in the right folder, and have the right data for the csv.  
        and makes a csv for each major.
    The csv has all the data in each of the major data dicts, the course names, the course codes, and the hours.

    In addition in the CSV the heading has the degree name, schoool name, and the University of texas at Austin 
    '''
    # Eh just an upper division column question and then a yes or no for each one based n=on the course num tho.
    schoolname=schooldata[list(schooldata)[0]]
    schooldir=schoolname
    course_school_folder='/Users/shalevwiden/Downloads/Projects/degreeviz'
    print(schoolname)

    degreedata=makelistof_majordata_dicts(schooldata)



    #   get the upper division status and append it too


    # with this one, do something similar to the one above

print('make_majorcoursesonly_csvs:\n')    
make_majorcoursesonly_csvs(schooldata=archdata)
def makemajorcoursesexcelfiles(schooldata):
      pass