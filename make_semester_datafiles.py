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

        # this one is fixed 
        self.degreeviewfolderpath='/Users/shalevwiden/Downloads/Projects/degreeview'
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
            degreename=degreename.replace('/','-').strip()

            print(f'Starting process for {degreename} ')
            
            # kept as sugg link as continuity from make_makorcourses_csvs
            sugglink=self.schooldata[key]

            
            semesterdictionary=getallcourses_splitbysemester(suggcourse_link=sugglink)
            # now use this to write to csv files.
            # I can actually finish this fast
            
            degreefolderpath=os.path.join(self.schoolfilepath,degreename)
            # can change this quite easily
            semestercsvfilename=os.path.join(degreefolderpath,f'{degreename} semestercsvfile.csv')

            totalhours=0
            numberofsemesters=len(semesterdictionary)
            csvobjectdict={}                        
            print(f'csv object has been rest to {len(csvobjectdict)}\n\n\n\n\n\n\n')
            
            rowcount=0
            with open(semestercsvfilename,'w',newline='') as semestercsvfile:

                # .write stuff now mf
                # split up sems 1-4 and 5-8 lol
                writer=csv.writer(semestercsvfile)
                writer.writerow([f'{degreename}',"","","",f'{self.schoolname}',"The University of Texas at Austin"])
                writer.writerow(['','','','',''])
                # due to the complex nature of the rows this needs a csv object
                # this actually wont be necessary in excel. 
                writer.writerow(['','Course Code','Course Name','Hours','Category','Upper/Lower Division'])
                
                
                for semesternum in range(numberofsemesters):
                    semester=list(semesterdictionary)[semesternum]
                    # semester courses is a dictionary of its own as well
                    semestercourses=semesterdictionary[semester]
                    
                    csvobjectdict[rowcount]=[f'{semester}']
                    rowcount+=1
                    for coursenameindex in range(len(semestercourses)):

                        coursename=list(semestercourses)[coursenameindex]
                        # if its NOT a list of lists:
                        if len(semestercourses[coursename])==4 and not isinstance(semestercourses[coursename][0],list):
                            coursecode, coursehours, upperdivstatus, coursecategory=semestercourses[coursename]
                            csvobjectdict[rowcount]=["",coursecode,coursename,coursehours,coursecategory,upperdivstatus]
                            rowcount+=1
                            if coursehours!='':
                                totalhours+=int(coursehours)
                        
                        else:
                            listofcourses=semestercourses[coursename]
                            for i in range(len(listofcourses)):
                                coursecode, coursehours, upperdivstatus, coursecategory=listofcourses[i]
                                csvobjectdict[rowcount]=["",coursecode,coursename,coursehours,coursecategory,upperdivstatus]
                                rowcount+=1

                                if coursehours!='':
                                    totalhours+=int(coursehours)


                    # line between semesters
                    csvobjectdict[rowcount]=['','','','','']
                    rowcount+=1




                print(f'len csv object={len(csvobjectdict)}')
                for row in csvobjectdict:
                    writer.writerow(csvobjectdict[row])

                writer.writerow(['','',f'Total Hours: {totalhours}','',''])
                writer.writerow(['DegreeView','','','','','DegreeView'])

                # this is for those giant architecture majors and some engineering that take like 6 years
        

                



        

        print(f'Made a semestercsv for {degreename}:\n As {semestercsvfilename}')

    def make_horizontal_csvfiles(self):
         '''for each degree in school data make a csv thats horizontal with 4 semesters on each side.'''

         ''' Only works for degrees with 8 semesters. '''
         for i in range(1,len(self.schooldata)):
            
            key=list(self.schooldata)[i]
            degreename=key
            degreename=degreename.replace('/','-').strip()
            print(f'Starting process for {degreename} ')
            
            # kept as sugg link as continuity from make_makorcourses_csvs
            sugglink=self.schooldata[key]

            
            semesterdictionary=getallcourses_splitbysemester(suggcourse_link=sugglink)
            # now use this to write to csv files.
            # I can actually finish this fast
            
            degreefolderpath=os.path.join(self.schoolfilepath,degreename)
            # can change this quite easily
            semestercsvfilename=os.path.join(degreefolderpath,f'{degreename} semestercsvfile.csv')

            totalhours=0
            numberofsemesters=len(semesterdictionary)
            csvobjectdict={}                        
            print(f'csv object has been rest to {len(csvobjectdict)}\n\n\n\n\n\n\n')
            
            rowcount=0
            if numberofsemesters==8:
                # dont forget to put the w
                with open(semestercsvfilename,'w',newline='') as semestercsvfile:

                    # .write stuff now mf
                    # split up sems 1-4 and 5-8 lol
                    writer=csv.writer(semestercsvfile)
                    writer.writerow([f'{degreename}',"","",f'{self.schoolname}',"The University of Texas at Austin"])
                    writer.writerow(['','','','',''])
                    # due to the complex nature of the rows this needs a csv object
                    # this actually wont be necessary in excel. 
                    writer.writerow(['','Course Code','Course Name','Hours','Category','Upper/Lower Division','','','','','','','Course Code','Course Name','Hours','Category','Upper/Lower Division'])
                    
                    
                    for semesternum in range(numberofsemesters):
                        semester=list(semesterdictionary)[semesternum]
                        # semester courses is a dictionary of its own as well
                        semestercourses=semesterdictionary[semester]
                        
                        csvobjectdict[rowcount]=[f'{semester}']
                        rowcount+=1
                        for coursenameindex in range(len(semestercourses)):

                            coursename=list(semestercourses)[coursenameindex]
                            # if its NOT a list of lists:
                            if len(semestercourses[coursename])==4 and not isinstance(semestercourses[coursename][0],list):
                                coursecode, coursehours, upperdivstatus, coursecategory=semestercourses[coursename]
                                csvobjectdict[rowcount]=["",coursecode,coursename,coursehours,coursecategory,upperdivstatus]
                                rowcount+=1
                                totalhours+=int(coursehours)
                            
                            else:
                                listofcourses=semestercourses[coursename]
                                for i in range(len(listofcourses)):
                                    coursecode, coursehours, upperdivstatus, coursecategory=listofcourses[i]
                                    csvobjectdict[rowcount]=["",coursecode,coursename,coursehours,coursecategory,upperdivstatus]
                                    rowcount+=1


                        # line between semesters
                        csvobjectdict[rowcount]=['','','','','']
                        rowcount+=1


                        # all of this is more to the right. 
                        # for semesternum in range(5,9):
                        #     # now use addnum to append, and see if this works...
                        #     addnum=semesternum=5
                        #     # well lets do that, csvobjectdict of semesternum+1
                        #     csvobjectdict[].append(['','','','','',f'{semester} MARKER'])
                        #     for coursenameindex in range(len(semestercourses)):

                        #         coursename=list(semestercourses)[coursenameindex]
                        #         # if its NOT a list of lists:
                        #         if len(semestercourses[coursename])==4 and not isinstance(semestercourses[coursename][0],list):
                        #             coursecode, coursehours, upperdivstatus, coursecategory=semestercourses[coursename]
                        #             csvobjectdict.append(["",coursecode,coursename,coursehours,coursecategory,upperdivstatus])
                        #             totalhours+=int(coursehours)
                                
                        #         else:
                        #             listofcourses=semestercourses[coursename]
                        #             for i in range(len(listofcourses)):

                        #                 coursecode, coursehours, upperdivstatus, coursecategory=listofcourses[i]
                        #                 csvobjectdict.append(["",coursecode,coursename,coursehours,coursecategory,upperdivstatus])


                        #     csvobjectdict.append(['','','','',''])




                    print(f'len csv object={len(csvobjectdict)}')
                    for row in csvobjectdict:
                        writer.writerow(csvobjectdict[row])

                    writer.writerow(['','',f'Total Hours: {totalhours}','',''])
                    writer.writerow(['DegreeView','','','',''])

                    # this is for those giant architecture majors and some engineering that take like 6 years
        
    def make_excel_files(self):
        '''
        This uses the result of the scrape semester data function to make an excel file out of it.
        For the CSV files I did them fully vertical. For these excel files, since I can control what columns and cells things are going,
        I want it to be more of a horizontal feel. 

        '''
        for i in range(1,len(self.schooldata)):
            key=list(self.schooldata)[i]
            degreename=key
            
            # kept as sugg link as continuity from make_makorcourses_csvs
            sugglink=self.schooldata[key]

            
            semesterdictionary=getallcourses_splitbysemester(suggcourse_link=sugglink)
            # now use this to write to csv files.
            # I can actually finish this fast
            semesterdictionary=splitupsemesters(createdsemesterdictionary=semesterdictionary)
            
            degreefolderpath=os.path.join(self.schoolfilepath,degreename)
            semestercsvfile=os.path.join(degreefolderpath,f'{degreename} semesterexcelfile.csv')

def make_mermaid_files(self):
        pass















workingdir=os.getcwd()
print(f'Working dir:{workingdir}')
# archdata testing
archdata=theasset[0]

archschoolkey=list(archdata)[0]
archschoolname=archdata[archschoolkey]
# print(f'School key: {archschoolkey}. School name: {archschoolname}')

architecturefiles=makeSemesterFiles(schooldata=archdata)
print('Testing:\nArchitecture School Folder Path')
print(architecturefiles.schoolfilepath)
print('Testing:\nArchitecture School Name')

print(getattr(architecturefiles,'schoolname'))
print('Making CSV files now:\n')
architecturefiles.makecsvfiles()


def unpacktheasset_into_makefilesclass(theasset):
    for schooldict in theasset:
        schoolobject=makeSemesterFiles(schooldata=schooldict)
        # make csvs for every school
        schoolobject.makecsvfiles()
unpacktheasset_into_makefilesclass(theasset=theasset)

# for a later document where I do this same thing but replicated. For this I will simply just modify the "make_majorcourses_csvs.py"
class makeMajorFiles:
    def __init__(self):
        pass