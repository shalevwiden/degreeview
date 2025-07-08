import os
import csv
import sys
import shutil

from theassetcontainment import theasset
'''
This one makes the SCHOOL SPECIFIC csvs (and future files), not degree specific like the other files
'''
# the asset is a list of dictionaries
def getstats():
    print(len(theasset))
    print('The asset has 14 schools')
    totalmajors=0
    for collegedict in theasset:
        majors=len(collegedict)-1
        if majors>1:
            print(f'There are {majors} majors in {collegedict['School_Name']}')
        else:
            print(f'There is {majors} major in {collegedict['School_Name']}')

        totalmajors+=(majors)
    print(f'\nThere are {totalmajors} majors')

    print('\n')

print(getstats())
print('Architecture Major Names from theasset:\n')
for i in theasset[0]:
    print(i)

arch_data=theasset[0]
# a way to get the schoolname without knowing the key
arcschoolname=arch_data[list(arch_data)[0]]

# schooldata is a dict

def makecsv(schooldata):
    '''school data is a dictionary, typically derived from one of the dictionaries in the asset.'''
    with open('architecture.csv','w',newline='') as archcsv:
        writer=csv.writer(archcsv)
        # first value               first key
        schoolname=schooldata[list(schooldata)[0]]
        writer.writerow([schoolname, "The University of Texas at Austin"])
        writer.writerow(['',''])

        writer.writerow(["Degree","URL to Suggested Arrangement of Courses Page"])
        # removed extra space
        for i in range(1,len(schooldata)):
            key=list(schooldata)[i]
            value=schooldata[key]
            writer.writerow([key,value])
        writer.writerow(['',''])
        writer.writerow(['degreeview'])




# makecsv(arch_data)


def automate_csvs(schooldata,directorypath):
    '''
    school data is a dictionary, typically derived from one of the dictionaries in the asset.
    This is later called in the below unpack function.
    '''
    schoolname=schooldata[list(schooldata)[0]]

    # no point to trying to not have spaces, as the school names all have spaces in them 
    filename=f'{schoolname} Degrees'
    filepath=f'{directorypath}/{filename}'
    with open(f'{filepath}.csv','w',newline='') as filename:
        writer=csv.writer(filename)
        # first value               first key
        writer.writerow([schoolname, "The University of Texas at Austin"])
        writer.writerow(['',''])

        writer.writerow(["Degree","URL to Suggested Arrangement of Courses Page"])
        for i in range(1,len(schooldata)):
            key=list(schooldata)[i]
            value=schooldata[key]
            writer.writerow([key,value])
        writer.writerow(['',''])
        writer.writerow(['',''])
        writer.writerow(['DegreeView'])

def unpack_the_asset_into_csvs(the_asset):
    # enter this as an argument to automate csvs
    course_csv_folder='/Users/shalevwiden/Downloads/Projects/degreeview'
    for schooldict in the_asset:
        try:
        # first make a folder for every school
            schoolname=schooldict[list(schooldict)[0]]
            schooldirpath=os.path.join(course_csv_folder, f'{schoolname}')
            # cant assign schooldirpath to mkdir

            # IMPORTANT: this can recreate the school folders if they are deleted 
            if not os.path.exists(schooldirpath):
                os.mkdir(schooldirpath)
                print(f'Made a new school dir at {schooldirpath}')

            print(schooldirpath)


            # then make the csvs per major for that school
            automate_csvs(schooldata=schooldict,directorypath=schooldirpath)
            print(f'\nMade a csv for {schoolname} majors at:\n {schooldirpath}\n ')
        except FileExistsError:
            print('File exists')

# gotta bust out the delete files script. 

# every time I run this file(makecsvs.py) it makes new csvs because of this line. 
unpack_the_asset_into_csvs(the_asset=theasset)
print('Unpacked')

# import the function I made in the adjacent file
from getall_suggestedcoursespages import getcollegenames
# have to do this printing stuff - add if name ==main to both files
if __name__=="__main__":
    print('imported "getcollegenames" function \n')
    print('\ndamn this works',"the colleges following are in UT:\n")
    print(getcollegenames())