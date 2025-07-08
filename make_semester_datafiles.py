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


# this script is gonna be.. huge
# the asset is a LIST of dictionaries
from theassetcontainment import theasset

from scrapesemesterdata import getallcourses_splitbysemester
from scrapesemesterdata import splitupsemesters


class makeSemesterFiles:
    '''
    Each object of this class should take an item (list item) from the asset.
    The asset of 0-14 for each school. 
    For testing we will use the asset of 0.
   
    '''
    # school data is like theasset[0], which is what each class object takes
    def __init__(self,schooldata):

        # you can print every attribute in the class which is the superpower tho. 

        # use self to make things an attribute
        self.schooldata=schooldata
        
        self.schoolnamekey=list(schooldata)[0]
        self.schoolname=schooldata[self.schoolnamekey]
        self.degreeviewfolderpath=os.path.abspath('degreeview')
        # this should work. If not I need to find a mystery
        self.schoolfilepath=os.path.join(self.degreeviewfolderpath,self.schoolname)


   
    def makecsvfiles(self):
        '''
        This uses the result of the scrape semester data function to make a csv file out of it.
        '''

        # for each degree in school data
        for i in range(1,len(self.schooldata)):
            key=list(self.schooldata)[i]
            degreename=key
            
            # kept as sugg link as continuity from make_makorcourses_csvs
            sugglink=self.schooldata[key]

            
            semesterdictionary=getallcourses_splitbysemester(suggcourse_link=sugglink)
            # now use this to write to csv files.
            # I can actually finish this fast
            splitupsemesterdict=splitupsemesters(createdsemesterdictionary=semesterdictionary)
            
            degreefolderpath=os.path.join(self.schoolfilepath,degreename)
            # can change this quite easily
            semestercsvfile=os.path.join(degreefolderpath,f'{degreename}semestercsvfile.csv')

            totalhours=0
            numberofsemesters=len(splitupsemesterdict)
            
            if numberofsemesters==8:
                with open(semestercsvfile,newline='') as semestercsvfile:

                    # .write stuff now mf
                    # split up sems 1-4 and 5-8 lol
                    writer=csv.writer(semestercsvfile)
                    writer.writerow([f'{degreename}',"","",f'{self.schoolname}',"The University of Texas at Austin"])
                    writer.writerow(['','','','',''])
                    # due to the complex nature of the rows this needs a csv object
                    # this actually wont be necessary in excel. 
                    csvobject=[]
                    for semesternum in range(len(splitupsemesterdict)):
                        semester=list(splitupsemesterdict)[semesternum]
                        # semester courses is a dictionary of its own as well
                        semestercourses=splitupsemesterdict[semester]
                        
                        csvobject.append(['','Course Code','Course Name','Hours','Category','Upper/Lower Division'])
                        if semesternum <=4:
                            csvobject.append([f'{semester}'])
                            for coursenameindex in range(len(semestercourses)):

                                coursename=list(semestercourses)[coursenameindex]

                                coursecode, coursehours, upperdivstatus, coursecategory=semestercourses[coursename]
                                csvobject.append(["",coursecode,coursename,coursehours,coursecategory,upperdivstatus])
                                totalhours+=int(coursehours)
                            csvobject.append(['','','','',''])

                        csvobject.append(['','','','','','','Course Code','Course Name','Hours','Category','Upper/Lower Division'])

                        # all of this is more to the right. 
                        elif semesternum>4:
                            
                            csvobject.append(['','','','','',f'{semester}'])
                            for coursenameindex in range(len(semestercourses)):

                                coursename=list(semestercourses)[coursenameindex]

                                coursecode, coursehours, upperdivstatus, coursecategory=semestercourses[coursename]
                                csvobject.append(["",'','','','','',coursecode,coursename,coursehours,coursecategory,upperdivstatus])

                                totalhours+=int(coursehours)
                        csvobject.append(['','','','',''])



                    writer.writerow(['','',f'Total Hours: {totalhours}','',''])
                    writer.writerow(['DegreeView','','','',''])

                    # this is for those giant architecture majors and some engineering that take like 6 years
            elif numberofsemesters>8:
                print('PLACEHOLDER') 





        print(f'Made a semestercsv for {degreename}:\n As {semestercsvfile}')


    def make_excel_files(self):
        '''
        This uses the result of the scrape semester data function to make an excel file out of it.

        '''
        for i in range(1,len(self.schooldata)):
            key=list(self.schooldata)[i]
            degreename=key
            
            # kept as sugg link as continuity from make_makorcourses_csvs
            sugglink=self.schooldata[key]

            
            semesterdictionary=getallcourses_splitbysemester(suggcourse_link=sugglink)
            # now use this to write to csv files.
            # I can actually finish this fast
            splitupsemesterdict=splitupsemesters(createdsemesterdictionary=semesterdictionary)
            
            degreefolderpath=os.path.join(self.schoolfilepath,degreename)
            semestercsvfile=os.path.join(degreefolderpath,f'{degreename}semesterexcelfile.csv')

def make_mermaid_files(self):
        pass















# archdata testing
archdata=theasset[0]

archschoolkey=list(archdata)[0]
archschoolname=archdata[archschoolkey]
# print(f'School key: {archschoolkey}. School name: {archschoolname}')

architecturefiles=makeSemesterFiles(schooldata=archdata)

def unpacktheasset_into_makefilesclass(theasset):
    pass
# for a later document
class makeMajorFiles:
    def __init__(self):
        pass