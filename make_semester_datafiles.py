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




    def make_excel_files(self):
        '''
        This uses the result of the scrape semester data function to make an excel file out of it.

        '''
        pass

def make_mermaid_files(self):
        pass
















archdata=theasset[0]
archschoolkey=list(archdata)[0]
archschoolname=archdata[archschoolkey]
print(f'School key: {archschoolkey}. School name: {archschoolname}')


# for a later document
class makeMajorFiles:
    def __init__(self):
        pass