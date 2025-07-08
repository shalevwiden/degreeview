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

    Essentially its a dictionary where the key is the degree name and the value is a dictionary 
    that is provided by the find_major_coursedata function
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




def make_majorcoursesonly_csvs(schooldata):
    '''
    this function doesnt take a list of major data dicts returned by the function above.
    But does call it. It has to take the schooldata dict so it can be placed in the right folder, and have the right data for the csv.  
        and makes a csv for each major.
    The csv has all the data in each of the major data dicts, the course names, the course codes, and the hours.

    In addition in the CSV the heading has the degree name, schoool name, and the University of texas at Austin 
    Important: the schooldata being entered is all data for a college, or one piece of the asset. 

    I dont really need a directory path since we are looking for already created folders in the directory.


    This function doesnt return anything
    '''
    # Eh just an upper division column question and then a yes or no for each one based n=on the course num tho.
    schoolname=schooldata[list(schooldata)[0]]
    schooldir=schoolname
    degreeviewfolder='/Users/shalevwiden/Downloads/Projects/degreeview'

    print(schoolname)
    listoffolders=os.listdir(degreeviewfolder)
    print(f'list of folders is {listoffolders}')

    # the [0] gets the first and only element
    schoolfolder=[folder for folder in listoffolders if folder==schooldir][0]
    print(f'\nCurrent folder is {schoolfolder}\n')


    

    # find the already created school folder where I will create a new folder there...
    degreesdata=makelistof_majordata_dicts(schooldata)
    # for each degree in the entire schools daya
    for degreedata in degreesdata:
         (degreename, majordatadict),=degreedata.items()

        # remove all slashes from the degree name so it doesnt mess up the mkdir command

         degreename=degreename.replace('/','-')    
         print(degreename+'\n')

        #  make a new folder for all data we will put for each degree.  - degreename folder
        # school folder should already exist
         degreefolderpath=f'{degreeviewfolder}/{schoolfolder}/{degreename}'
        
        # if it doesnt exist create it. If it does exist, we'll go make it regardless. 
        # degree folders, not school folders being made here
         if not os.path.exists(degreefolderpath):
            os.mkdir(degreefolderpath)

         majors_csvfile_name=f'{degreename} Courses.csv'

         fullpath=f'{degreefolderpath}/{majors_csvfile_name}'

         with open(fullpath,'w',newline='') as majors_csvfile:
            writer=csv.writer(majors_csvfile)
            writer.writerow([f'{degreename}',"","",f'{schoolname}',"The University of Texas at Austin"])
            writer.writerow(['','','','',''])
            writer.writerow(['Course Code','Course Name','Hours','Upper/Lower Division'])


            # I want to add the ones with no coursecodes last
            addlast={}

            # iterate over the keys in major data dict, which is each coursename
            totalhours=0
            for coursename in majordatadict:
                #   if its not a repeat course like the "upper division major course" ones
                
                # check if the first item of the value is not a list. It should be a string if it has has coursecode.
                if len(majordatadict[coursename])==3 and not isinstance(majordatadict[coursename][0],list):
                    
                    coursecode, coursehours, upperdivstatus=majordatadict[coursename]
                    # Modify this in the future to change how the data appears
                    writer.writerow([coursecode,coursename,coursehours,upperdivstatus])
                    totalhours+=int(coursehours) if coursehours.strip() else 0
                    
                else: #those lists of lists
                    listofupperdivcoursedata=majordatadict[coursename]
                    addlast[coursename]=listofupperdivcoursedata
                    # add it to the add last

            # add last should really only be len()=1
            for coursename in addlast:
                for courseentry in addlast[coursename]:
                    coursecode, coursehours, upperdivstatus=courseentry
                    # Modify this in the future to change how the data appears
                    writer.writerow([coursecode,coursename,coursehours,upperdivstatus])
                    totalhours+=int(coursehours) if coursehours.strip() else 0


            # footer in the csv
            writer.writerow(['','',f'Total Major Hours: {totalhours}','',''])
            writer.writerow(['DegreeView','','','',''])


            print(f'\n\nMade {fullpath}\n\n')

    #   get the upper division status and append it too


    # with this one, do something similar to the one above
def unpacktheasset_into_majorcoursesonlycsvs(theasset):
    for schooldict in theasset:
        schoolname=schooldict[list(schooldict)[0]]

        make_majorcoursesonly_csvs(schooldata=schooldict)
        print(f'Made major csvs for {schoolname}')

    
if __name__=='__main__':

    print('testing:\n')
    print('test the find_major_coursedata function again')


    cssuggestedarrangement=requests.get('https://catalog.utexas.edu/undergraduate/natural-sciences/degrees-and-programs/bs-computer-science/sugg-comp-sci-bscompsci/')
    cssoup=BeautifulSoup(cssuggestedarrangement.text,'html.parser')
    print(find_major_coursedata(course_soup=cssoup))
    print('\nNow iterate over the CS major course data:\n')
    csmajorcoursedata=find_major_coursedata(course_soup=cssoup)
    for coursecode in csmajorcoursedata:
         print(f'\n{coursecode}\n')
    print('\nMakelistof_majordata_dicts following\n')
    print('Big list testing:')

    

    biglist=makelistof_majordata_dicts(archdata)

    for i in biglist:
        print(f'\n{i}\n')
    print('\n\nmake_majorcoursesonly_csvs (the big function):\nThis should print testing data while I work:\n')    
   
    make_majorcoursesonly_csvs(schooldata=archdata)

    print('\nUnpacking the asset and creating major only CSVs\n')
    unpacktheasset_into_majorcoursesonlycsvs(theasset=theasset)

def makemajorcoursesexcelfiles(schooldata):
      pass
      #just take the make_majorcoursesonly_csvs function and modify it
    #   hmm I might as well just install openpy_xl in this venv. 
    # 
      


# probably do this in another file and just import
def makemajoronly_mmdfiles(schooldata):
    ''' use a similar approach to makemajoronly csvs
    in that I can use that biglist'''
    pass