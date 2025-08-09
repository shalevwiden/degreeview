
import sys
import os
import subprocess
import random

import csv
import sqlite3

# all this just to get the asset
# but be something else besides config for the name
import importlib.util 
file_path = '/Users/shalevwiden/Downloads/Coding_Files/Python/BeautifulSoup_Library/college_course_scraping/theassetcontainment.py'

spec = importlib.util.spec_from_file_location("config", file_path)
config = importlib.util.module_from_spec(spec)
spec.loader.exec_module(config)

theasset=config.theasset
degreeviewfolder='/Users/shalevwiden/Downloads/Projects/degreeview'
archfolder='/Users/shalevwiden/Downloads/Projects/degreeview/School of Architecture'


def lengthanalysis(folderpath):
    '''This does quieries on the databases for every degree to get the longest and shortest coursenames'''
    
    schoollengthlist=[]
    for root,folders,files in os.walk(folderpath):
        
        for file in files:
            if file.endswith(".db"):
                fullpath=os.path.join(root,file)

                # this gets the last part
                degreefoldername = os.path.basename(root)
                degreename=degreefoldername.replace('-','/')

                # degreenamecleaned is in the database name(file)
                degreenamecleaned=file.replace('-database.db',"")
                tabledegreename=degreenamecleaned.replace('-','_').replace(',','_').replace('&','and').replace("'","")
                tablename=f'{tabledegreename}_table'

                with sqlite3.connect(fullpath) as conn:

                    '''
                    Find the longest coursename in the "Coursename" named column.

                    the LIMIT 1 means it will only return the top 1 in the tuple 
                    '''

                    cursor=conn.cursor()
                    longestnamecommand=f'''
                    SELECT Coursename 
                    FROM {tablename} 
                    WHERE Coursename IS NOT NULL AND Coursename != ''
                    ORDER BY LENGTH(Coursename) DESC LIMIT 1;'''

                    cursor.execute(longestnamecommand)
                    longestresult=cursor.fetchone()[0]

                    shortestnamecommand=f'''
                    SELECT Coursename 
                    FROM {tablename} 
                    WHERE Coursename IS NOT NULL AND Coursename != ''
                    ORDER BY LENGTH(Coursename) ASC LIMIT 1;'''

                    cursor.execute(shortestnamecommand)

                    shortestresult=cursor.fetchone()[0]

                    # print(f'\nData for {degreename}:\n')
                    # print(shortestresult)
                    # print(longestresult)

                    schoollengthlist.append([degreename,shortestresult,longestresult])
    
    return schoollengthlist

lengthanalysis(folderpath=archfolder)

def make_length_list():
    # borrowed from make_semester_datafiles.py

    lengthlist=[]
    for schooldata in theasset:

        schoolnamekey=list(schooldata)[0]
        schoolname=schooldata[schoolnamekey]

        # this one is fixed 
        degreeviewfolderpath='/Users/shalevwiden/Downloads/Projects/degreeview'
        # this should work. If not I need to find a mystery
        schoolfolderpath=os.path.join(degreeviewfolderpath,schoolname)
        print(f'\nRunning Length analysis for {schoolname}\n')
        resultlist=lengthanalysis(folderpath=schoolfolderpath)
        lengthlist+=resultlist
    return lengthlist

print(f'Length List\n')
lengthlist=make_length_list()

lengthlistsorted_long=sorted(lengthlist,key=lambda x:len(x[2]),reverse=True)
# print(lengthlistsorted_long)

lengthlistsorted_short=sorted(lengthlist,key=lambda x:len(x[1]))

print("Longest Course Name:\n")
print(lengthlistsorted_long[0],len(lengthlistsorted_long[0][2]))

def make_length_csv():

    lengthlist=make_length_list()
    lengthlistsorted_long=sorted(lengthlist,key=lambda x:len(x[2]),reverse=True)
    lengthlistsorted_short=sorted(lengthlist,key=lambda x:len(x[1]))


    with open('/Users/shalevwiden/Downloads/Projects/degreeview/stats/longest_courselengths.csv','w') as file:
        writer=csv.writer(file)
        writer.writerow(['Degreename','Coursename','Length of Coursename'])

        for list in lengthlistsorted_long:
            degreename, shortestresult, longestresult=list    
            writer.writerow([degreename,longestresult,len(longestresult)])

    with open('/Users/shalevwiden/Downloads/Projects/degreeview/stats/shortest_courselengths.csv','w') as file:
        writer=csv.writer(file)
        writer.writerow(['Degreename','Coursename','Length of Coursename'])

        for list in lengthlistsorted_short:
            degreename, shortestresult, longestresult=list    
            writer.writerow([degreename,shortestresult,len(shortestresult)])
        




def countcourses(folderpath):
    '''This does quieries on the databases for every degree to get the longest and shortest coursenames'''
    '''Important: takes a SCHOOL folder path.'''
    
    schoolcount=0
    for root,folders,files in os.walk(folderpath):
        
        for file in files:
            # this gets all the databases. But theres only databases for each degreeplan, so it works. 
            if file.endswith(".db"):
                fullpath=os.path.join(root,file)

                # this gets the last part
                degreefoldername = os.path.basename(root)
                degreename=degreefoldername.replace('-','/')

                # degreenamecleaned is in the database name(file)
                degreenamecleaned=file.replace('-database.db',"")
                # this is for cleaning the name for the table which is very specific
                tabledegreename=degreenamecleaned.replace('-','_').replace(',','_').replace('&','and').replace("'","")
                tablename=f'{tabledegreename}_table'

                with sqlite3.connect(fullpath) as conn:

                    '''
                    Find coursecount in the "Coursename" named column.

                    '''
                    cursor=conn.cursor()

                    length_course_column_command=f'''
                    SELECT COUNT(*) 
                    FROM {tablename} 
                    WHERE Coursename IS NOT NULL AND Coursename != '';
                    '''

                    cursor.execute(length_course_column_command)

                    degreecount=cursor.fetchone()[0]
                    schoolcount+=degreecount
                    

    print(f'School course count for {os.path.basename(folderpath)}: {schoolcount}')
    return schoolcount


def countallcourses():
    # borrowed from make_semester_datafiles.py

    totalcount=0
    for schooldata in theasset:

        schoolnamekey=list(schooldata)[0]
        schoolname=schooldata[schoolnamekey]

        # this one is fixed 
        degreeviewfolderpath='/Users/shalevwiden/Downloads/Projects/degreeview'

        # this should work. 
        schoolfolderpath=os.path.join(degreeviewfolderpath,schoolname)
        
        # print(f'\nRunning Course analysis for {schoolname}\n')
        coursecount=countcourses(folderpath=schoolfolderpath)
        totalcount+=coursecount
    return totalcount

totalcourses=countallcourses()
print(f'\nTotal courses (on suggested arrangement of courses page): {totalcourses}')
