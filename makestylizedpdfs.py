import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os
import subprocess
import random

import csv
import openpyxl




from openpyxl import load_workbook
from openpyxl import Workbook
# use this to define the function define_start_column
from openpyxl.utils import column_index_from_string

# this assigns cells colors
from openpyxl.styles import PatternFill

import time
import os

from openpyxl.styles import Font
from openpyxl.styles import Border, Side, Alignment

# for working with pdfs:
import cairosvg
from cairosvg import svg2pdf

# png to pdf conversion
from PIL import Image


from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.colors import Color


# for merging the pdfs: and reading them to get data. 
from PyPDF2 import PdfMerger, PdfReader, PdfWriter
from pathlib import Path  


# for database stuff
import sqlite3


# Define the absolute path to the folder containing the file you want to import
# Replace this with your actual absolute path
pdftemplatesfolder = Path('/Users/shalevwiden/Downloads/Coding_Files/Python/BeautifulSoup_Library/PDF_Templates')

# Add the folder to the front of sys.path so Python will search here first
sys.path.insert(0, str(pdftemplatesfolder))

# Now you can import the function as if it were local
from stareoverlay import create_stare_png

from dolphinoverlay import create_dolphin_png



# good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'the version of openpyxl is\n {(openpyxl.__version__)}')

    print(f'\nthe python version being used is:{sys.executable}\n')


# this script is gonna be.. huge. Yeah this is the behemoth one
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

        # this one is fixed 
        self.degreeviewfolderpath='/Users/shalevwiden/Downloads/Projects/degreeview'
        # this should work. If not I need to find a mystery
        self.schoolfolderpath=os.path.join(self.degreeviewfolderpath,self.schoolname)
        
        self.schoolcolordict={'School of Architecture':'#cdbee9', 'Red McCombs School of Business':'#f9e4af', 
 'School of Civic Leadership':'#096c6c', 'Moody College of Communication':'#7e0107',
   'College of Education':'#86dff5', 'Cockrell School of Engineering':'#e35501', 
   'College of Fine Arts':"#633224", 'John A. and Katherine G. Jackson School of Geosciences':'#a3d29c', 
   'School of Information':'#2bc5e0', 
 'College of Liberal Arts':'#f3f3f3', 'College of Natural Sciences':'#f6c44b', 'School of Nursing':'#e3971f',
  'College of Pharmacy':"#BAB86C", 'Lyndon B. Johnson School of Public Affairs':'#096c6c', 'Steve Hicks School of Social Work':'#f0b420'}
        
        self.schoolcolor=self.schoolcolordict[self.schoolname]

        self.logopath='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/logo_design/logo6.png'


        # this might have to change later lol
        self.websiteurl_img_path='/Users/shalevwiden/Downloads/Projects/dvwebsitecreation/logo_design/websiteurl.png'

    def __str__(self):
        returnstring=f'This is an object to create files for {self.schoolname}'
        return returnstring
   
    def upload_to_database(self):
        '''
        
        Uses SQLite to upload to databases.
        We will then to quieries on said databases.

        
        '''
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
            
            degreefolderpath=os.path.join(self.schoolfolderpath,degreename)
            # can change this quite easily


            # its a little different from the database name, use underscore instead of hyphen
            degreenamecleaned=degreename.replace(' ','').lower().split('(')
            degreenamecleaned=degreenamecleaned[0]+"-"+degreenamecleaned[-1]
            degreenamecleaned=degreenamecleaned.replace(')','')

            

            databasepath=os.path.join(degreefolderpath,f'{degreenamecleaned}-database.db')
            # hyphens and commas not allowed in tablename
            tabledegreename=degreenamecleaned.replace('-','_').replace(',','_').replace('&','and').replace("'","")

            tablename=f'{tabledegreename}_table'
            def maketable():
                '''This creates the table for course data in the db'''
                with sqlite3.connect(databasepath) as conn:
                    cursor=conn.cursor()

                # table name lowercase
                    createtablecommand=f'''CREATE TABLE IF NOT EXISTS "{tablename}" (Coursecode TEXT , Coursename TEXT, Hours INT, Category TEXT, UpperDivStatus TEXT );'''
                    cursor.execute(createtablecommand)
                    conn.commit()
            maketable()
            totalhours=0
            numberofsemesters=len(semesterdictionary)
            

                # .write stuff now mf
                # split up sems 1-4 and 5-8 lol
                
            with sqlite3.connect(databasepath) as conn:
                cursor=conn.cursor()

                    
                for semesternum in range(numberofsemesters):
                    semester=list(semesterdictionary)[semesternum]
                    # semester courses is a dictionary of its own as well
                    semestercourses=semesterdictionary[semester]
                        
                    for coursenameindex in range(len(semestercourses)):

                        coursename=list(semestercourses)[coursenameindex]
                            # if its NOT a list of lists:
                        if len(semestercourses[coursename])==4 and not isinstance(semestercourses[coursename][0],list):
                            coursecode, coursehours, upperdivstatus, coursecategory=semestercourses[coursename]
                            cursor.execute(f'INSERT INTO {tablename} (Coursecode, Coursename, Hours, Category, UpperDivStatus) values(?,?,?,?,?);',
                                   [coursecode,coursename,coursehours,coursecategory,upperdivstatus])
                            

                            if coursehours!='':
                                totalhours+=int(coursehours)
                            
                        else:
                            listofcourses=semestercourses[coursename]
                            for i in range(len(listofcourses)):
                                coursecode, coursehours, upperdivstatus, coursecategory=listofcourses[i]
                                cursor.execute(f'INSERT INTO {tablename} (Coursecode, Coursename, Hours, Category, UpperDivStatus) values(?,?,?,?,?);',
                                   [coursecode,coursename,coursehours,coursecategory,upperdivstatus])

                                if coursehours!='':
                                    totalhours+=int(coursehours)


                    # empty line between semesters
                    cursor.execute(f'INSERT INTO {tablename} (Coursecode, Coursename, Hours, Category, UpperDivStatus) values(?,?,?,?,?);',
                                   [None,None,None,None,None])
                                   
                 # commit to the database 
                conn.commit()
                print(f'Created {degreenamecleaned}-database.db\n')
                





        
    def make_mermaid_files(self):

# we start at 1 because 0 is the school name 
        for i in range(1,len(self.schooldata)):

        # in this entire folder we are doing things by degree.


            key=list(self.schooldata)[i]
            degreename=key
            degreename=degreename.replace('/','-').strip()

            print(f'Starting process for {degreename} mermaid file')
            
            # kept as sugg link as continuity from make_makorcourses_csvs
            sugglink=self.schooldata[key]

            
            semesterdictionary=getallcourses_splitbysemester(suggcourse_link=sugglink)
            # now use this to write to csv files.
            # I can actually finish this fast
            
            degreefolderpath=os.path.join(self.schoolfolderpath,degreename)
            # can change this quite easily
            # theres spaces which isnt great. But theres also spaces in the degreename. 

            diagram_folder=os.path.join(degreefolderpath,'diagrams_and_mmdstuff')
            if not os.path.exists(diagram_folder):
                os.mkdir(diagram_folder)

            # this is reassigned later anyway
            mermaid_file_path=os.path.join(diagram_folder,f'{degreename} semesterdiagram.mmd')
            

            totalhours=0
            numberofsemesters=len(semesterdictionary)
            diagramcode = '''
        graph TD
            '''
            # top down graph
            # layout stuff? fixed, automatic. 

        # flowchart:
            # curve: basis

            hexpicker="#cf840c"
            

            # establish classes
            title_class_name='title_class'
            hiddencolor='#fff'
            title_class=f'   \n  classDef title_class fill:{hiddencolor},stroke:{hiddencolor},stroke-width:5px,color:{hiddencolor},font-size:26px,font-weight:bold,width:260px,padding:20px,text-align:center,rx:20,ry:20'


            diagramcode+=title_class

            major_cat_class_name='major_cat_class'
            major_cat_class='   \nclassDef major_cat_class fill: #1d79db, stroke:#fff,stroke-width:4px,color:#FFF,font-weight:bold,rx:20,ry:20' 
            #stroke is border.
            diagramcode+=major_cat_class

            core_cat_class_name='core_cat_class'
            core_cat_class='    \nclassDef core_cat_class  fill:#BF5706, stroke:#fff,stroke-width:4px,color:#FFF,font-weight:bold;'
            diagramcode+=core_cat_class

            # I can manually make this bigger with spaces

            more_than_3_class='     \nclassDef more_than_3_class  fill:#f96, color:#FFF,font-weight:bold,stroke:#fff,stroke-width:4px;'


            elective_cat_class_name="elective_cat_class"
            elective_cat_class='    \nclassDef elective_cat_class  color:#FFF,font-weight:bold,fill:#579d42, stroke:#fff,stroke-width:4px;'
            diagramcode+=elective_cat_class

            gened_cat_class_name='gened_cat_class'
            gened_cat_class='    \nclassDef gened_cat_class color:#FFF,font-weight:bold,fill:#ae6455, stroke:#fff,stroke-width:4px;'
            diagramcode+=gened_cat_class


            opportunity_cat_class_name='opportunity_cat_class'
            opportunity_cat_class='    \nclassDef opportunity_cat_class color:#FFF,font-weight:bold,fill:#f2bb16, stroke:#fff,stroke-width:4px;'
            diagramcode+=opportunity_cat_class

            other_class_name='other_class'
            other_class= '  \nclassDef other_class color:#FFF,font-weight:bold,fill:#9cadb7, stroke:#fff,stroke-width:4px;'
            diagramcode+=other_class
            # 

        # at the end add everything connection. For now I define the subgraph. I'll be able to set arrow styles and such too.

            # use coursecount to make stuff invisible
            coursecount=0
            totalhours=0
            arrowcount=0
            # for each semester
            # do 1 and then +1 why?
            for semesternum in range(numberofsemesters):
                semester=list(semesterdictionary)[semesternum]
                semestercourses=semesterdictionary[semester]

                # the subgraph will have the text 1st semester, 2nd semester, etc but names semester1, semester2, etc
                diagramcode+=f'    \n\nsubgraph semester{semesternum+1}[{semester}]\n'

                
            
                
                # this is looping through the courses PER semester
                keeparrowlist=[]
                keeparrowlist=[item+2 for item in keeparrowlist]

                courseinsemestercount=0
                for coursenameindex in range(len(semestercourses)):

                    coursename=list(semestercourses)[coursenameindex]
                    # node name must be unique
                    nodename=f'course{courseinsemestercount}semester{semesternum}' #keep in mind its 0 indexed

                    # this is like course1semester1

                    # if its NOT a list of lists:
                    if len(semestercourses[coursename])==4 and not isinstance(semestercourses[coursename][0],list):
                        coursecode, coursehours, upperdivstatus, coursecategory=semestercourses[coursename]

                        # adding to mermaid logic--------------



                        # now set the brackets based on category. Square, round, rounded, triangle, etc. 
                        # change all the shape types later and add more to the classes as well.

                        # CSS is a walk in the park compared to this...god


                        # and give them classes. 
                        if 'major' in coursecategory.lower():
                            diagramcode+=f'\n{nodename}("{coursecode}")\n'

                            # define the class in the mmd file

                            diagramcode+=f'\nclass {nodename} {major_cat_class_name}\n'
                            

                        elif 'core' in coursecategory.lower() and "major" not in coursecategory.lower():
                            diagramcode+=f'{nodename}(["{coursecode}"])\n'

                            diagramcode+=f'class {nodename} {core_cat_class_name}\n'

                        elif 'general education' in coursecategory.lower():
                            diagramcode+=f'{nodename}["{coursecode}"]\n'
                            diagramcode+=f'class {nodename} {gened_cat_class_name}\n'



                        elif 'elective' in coursecategory.lower():
                            diagramcode+=f'{nodename}{{{{"{coursecode}"}}}}\n'

                            diagramcode+=f'class {nodename} {elective_cat_class_name}\n'


                        elif 'opportunity' in coursecategory.lower():
                            diagramcode+=f'{nodename}>"{coursecode}"]\n'
                            diagramcode+=f'class {nodename} {opportunity_cat_class_name}\n'

                        else:
                            diagramcode+=f'{nodename}[{coursecode}]\n'
                            diagramcode+=f'class {nodename} {other_class_name}\n'



                        # ----------------------------------------------------------
                        courseinsemestercount+=1
                        if coursehours!='':
                            totalhours+=int(coursehours)

                    
                    else:
                        listofcourses=semestercourses[coursename]
                        for i in range(len(listofcourses)):
                            coursecode, coursehours, upperdivstatus, coursecategory=listofcourses[i]
                            # this works cause even if list is 1 in length itll still add
                            nodename=f'course{courseinsemestercount}semester{semesternum}'
                            courseinsemestercount+=1
                            

                            # coursename is an empty string so use coursename here
                            if 'major' in coursecategory.lower():
                                diagramcode+=f'\n{nodename}("{coursename}")\n'

                            # define the class in the mmd file

                                diagramcode+=f'\nclass {nodename} {major_cat_class_name}\n'
                            

                            elif 'core' in coursecategory.lower() and "major" not in coursecategory.lower():
                                diagramcode+=f'{nodename}(["{coursename}"])\n'

                                diagramcode+=f'class {nodename} {core_cat_class_name}\n'

                            elif 'general education' in coursecategory.lower():
                                diagramcode+=f'{nodename}["{coursename}"]\n'
                                diagramcode+=f'class {nodename} {gened_cat_class_name}\n'



                            elif 'elective' in coursecategory.lower():
                                diagramcode+=f'{nodename}{{{{"{coursename}"}}}}\n'

                                diagramcode+=f'class {nodename} {elective_cat_class_name}\n'


                            elif 'opportunity' in coursecategory.lower():
                                diagramcode+=f'{nodename}>"{coursename}"]\n'
                                diagramcode+=f'class {nodename} {opportunity_cat_class_name}\n'

                            else:
                                diagramcode+=f'{nodename}[{coursename}]\n'
                                diagramcode+=f'class {nodename} {other_class_name}\n'




                            if coursehours!='':
                                totalhours+=int(coursehours)
                    coursecount+=courseinsemestercount
                # dealing with in subgraph stuff

                arrowmarker='---'
                if courseinsemestercount==4:
                    diagramcode+=f'course0semester{semesternum}{arrowmarker}course1semester{semesternum}\n'
                    diagramcode+=f'course2semester{semesternum}{arrowmarker}course3semester{semesternum}\n'
                    arrowcount+=2

                elif courseinsemestercount==5:
                    leftorright='left' if random.randint(0,1)==0 else 'right'
                    if leftorright=='left':
                        diagramcode+=f'course0semester{semesternum}{arrowmarker}course1semester{semesternum}{arrowmarker}course2semester{semesternum}\n'
                        diagramcode+=f'course3semester{semesternum}{arrowmarker}course4semester{semesternum}\n'
                        arrowcount+=3

                    else:
                        diagramcode+=f'course0semester{semesternum}{arrowmarker}course1semester{semesternum}\n'
                        diagramcode+=f'course2semester{semesternum}{arrowmarker}course3semester{semesternum}{arrowmarker}course4semester{semesternum}\n'
                        arrowcount+=3

                elif courseinsemestercount>=6:
                    diagramcode+=f'course0semester{semesternum}{arrowmarker}course1semester{semesternum}{arrowmarker}course2semester{semesternum}\n'
                    diagramcode+=f'course3semester{semesternum}{arrowmarker}course4semester{semesternum}{arrowmarker}course5semester{semesternum}\n'
                    arrowcount+=4

                    if courseinsemestercount==7:
                        diagramcode+=f'course6semester{semesternum}\n'


                    elif courseinsemestercount==8:
                        diagramcode+=f'course6semester{semesternum}\n'
                        diagramcode+=f'course7semester{semesternum}\n'


                    




                diagramcode+='\nend'
                diagramcode+='\n'
            # now connect the semesters:
            
            # see which semesters are on which sides
            firsthalf=numberofsemesters//2
            secondhalf=(numberofsemesters//2+firsthalf) if numberofsemesters%2==0 else ((numberofsemesters//2)+1)+firsthalf
            # change this 
            titlenode=f'\ntitlenode("{degreename} Semester Layout")\n'
            diagramcode+=titlenode
            diagramcode+=f'class titlenode {title_class_name}\n'

            # this connects to the right semester essentially
            diagramcode+=f'titlenode==>semester1\n'    
            # this should be respoonsive based on semester lengths

            diagramcode+=f'titlenode==>semester{secondhalf+1-firsthalf}\n'

            # make all arrows hidden except for the semester arrows...
            for arrowcount in range(arrowcount+2):
                diagramcode+=f'linkStyle {arrowcount} stroke:transparent,fill:transparent\n'

            
            # split up the halves        
            # 
            firsthalfconnected='\n  '
            keeparrowcount=0

            for semesternum in range(1,firsthalf+1):
                # changeline styles here 
                # for readability
                if semesternum==(firsthalf+1)-1:
                    firsthalfconnected+=f'semester{semesternum}=====>legend\n'
                else:
                    firsthalfconnected+=f'semester{semesternum}====>'
                    keeparrowcount+=1

            diagramcode+='%% firsthalfconnected:\n'
            diagramcode+=firsthalfconnected


            secondhalfconnected='\n '

            for semesternum in range(firsthalf+1,secondhalf+1):

                # changeline styles here 

                if semesternum==secondhalf+1-1:
                    secondhalfconnected+=f'semester{semesternum}=====>legend\n'
                else:
                    secondhalfconnected+=f'semester{semesternum}====>'
                    keeparrowcount+=1

            diagramcode+='%% secondhalfconnected:'

            diagramcode+=secondhalfconnected+'\n'

            # now hide the connecting to legend arrows:
            diagramcode+='%% Hide the connecting to legend arrows.\n'

            # this works...for some reason
            diagramcode+=f'linkStyle {arrowcount+firsthalf} stroke:transparent,fill:transparent\n'
            diagramcode+=f'linkStyle {arrowcount+keeparrowcount+2} stroke:transparent,fill:transparent\n'


            # legend and stats node
            # this one will be all flat on the bottom. 
            diagramcode+=f'    \n\nsubgraph legend["Course Legend"]\n'
            
            diagramcode+=f'''
        majornode("Major Category Courses")\n
        corenode(["Core Category Courses"])\n
        genednode["General Education Category Courses"]\n
        electivenode{{{{"Elective Category Courses"}}}}\n
        opportunitynode>"Opportunity Category Courses"]\n
        othernode["Other/Unspecified"]\n

        '''    
            diagramcode+='end\n'

            diagramcode+=f'\nclass majornode {major_cat_class_name}\n'
            diagramcode+=f'\nclass corenode {core_cat_class_name}\n'
            diagramcode+=f'\nclass genednode {gened_cat_class_name}\n'
            diagramcode+=f'\nclass electivenode {elective_cat_class_name}\n'
            diagramcode+=f'\n class opportunitynode {opportunity_cat_class_name}\n'
            diagramcode+=f'\n class othernode {other_class_name}'


            








        # --------------Now actually building the file and saving it -------------------------------------------------
            # replace this with the path to the schoolfolder in the right file


            degreenamecleaned=degreename.replace(' ','').lower().split('(')
            degreenamecleaned=degreenamecleaned[0]+"-"+degreenamecleaned[-1]
            degreenamecleaned=degreenamecleaned.replace(')','')

            mermaid_file_path=os.path.join(diagram_folder,f'{degreenamecleaned}-semesterdiagram.mmd')

            svg_savefilepath=os.path.join(diagram_folder,f'{degreenamecleaned}-semesterdiagram.svg')
            originaltheme_png_savefilepath=os.path.join(diagram_folder,f'{degreenamecleaned}-semesterdiagram.png')





            
            with open(mermaid_file_path, "w") as mermaidsemesterfile:
                mermaidsemesterfile.write(diagramcode)


            themepath=os.path.abspath('darktheme.json')

            lightthemeconfig="/Users/shalevwiden/Downloads/Coding_Files/Mermaid/Coursemmd/mermaid_config_files/light_congif_file.json"


            def rendermmd(createdpath,savepath,configpath):
                # adding a background here actually works
                # add this for dolphin: "--backgroundColor", "#a3dbf1ff"

                subprocess.run(["mmdc", "-i", createdpath, "-o", savepath,"--configFile",configpath,"--scale=3"])
            

            # create both svg and png
            def create_dolphin():
                rendermmd(createdpath=mermaid_file_path,savepath=originaltheme_png_savefilepath,configpath=lightthemeconfig)

                create_dolphin_png(imagepath=originaltheme_png_savefilepath,savepath=originaltheme_png_savefilepath)
            # create_dolphin()
            def createstare():
                rendermmd(createdpath=mermaid_file_path,savepath=originaltheme_png_savefilepath,configpath=lightthemeconfig)

                create_stare_png(imagepath=originaltheme_png_savefilepath,savepath=originaltheme_png_savefilepath)

            createstare()
            # create_dolphin_png(imagepath=originaltheme_png_savefilepath,savepath=originaltheme_png_savefilepath)

            print(f'Created {mermaid_file_path} and saved it at {originaltheme_png_savefilepath}')
            print(f'degreename is {degreename}')

            

    def create_mmd_pdfs(self,savename):

        '''
        This takes the pdfs or svgs created by the above function, and turns them into stylized pdfs.

        Above is where background and node styling can take place.

        Here is where logo, images, sizing, and page appendation can take place.

        This one only creates EVEN numbered semester pdfs.
        '''
        for i in range(1,len(self.schooldata)):

        # in this entire folder we are doing things by degree.


            key=list(self.schooldata)[i]
            degreename=key
            degreename=degreename.replace('/','-').strip()


            degreenamecleaned=degreename.replace(' ','').lower().split('(')
            degreenamecleaned=degreenamecleaned[0]+"-"+degreenamecleaned[-1]
            degreenamecleaned=degreenamecleaned.replace(')','')

            print(f'Starting process for {degreename} mermaid file')
            
            # kept as sugg link as continuity from make_makorcourses_csvs
            sugglink=self.schooldata[key]

            semesterdictionary=getallcourses_splitbysemester(suggcourse_link=sugglink)
            numberofsemesters=len(semesterdictionary)
            if numberofsemesters%2==0:


                
                # now use this to write to csv files.
                # I can actually finish this fast
                
                degreefolderpath=os.path.join(self.schoolfolderpath,degreename)
                # can change this quite easily
                # theres spaces which isnt great. But theres also spaces in the degreename. 

                diagram_folder=os.path.join(degreefolderpath,'diagrams_and_mmdstuff')
                
                originaltheme_png_file=os.path.join(diagram_folder,f'{degreenamecleaned}-semesterdiagram.png')

                legendonlypng_path='/Users/shalevwiden/Downloads/Coding_Files/Mermaid/Coursemmd/legendfolder/legendonly.png'

                originaltheme_pdf_file=os.path.join(diagram_folder,f'{degreenamecleaned}-semesterdiagram.pdf')


            # step one: convert pdfs to pngs.

                def png_to_pdf(png_path, pdf_path):
                    # Open the PNG and convert to RGB (PDFs can't handle alpha channels)
                    image = Image.open(png_path).convert("RGB")
                    image.save(pdf_path, "PDF")
                    print(f"Saved PDF to: {pdf_path}")
                
                # this is the diagram pdf.
                

                png_to_pdf(png_path=originaltheme_png_file,pdf_path=originaltheme_pdf_file)
                print(f'Created png to pdf for {originaltheme_pdf_file}')


                # This is the legend only pdf. The png is made in seperatelegend.py.

                def createmainoverlaypdf(diagrampath, outputpath):

                    # first get pdf data.
                    base_pdf = PdfReader(diagrampath)
                    page = base_pdf.pages[0]
                    width = float(page.mediabox.width)
                    height = float(page.mediabox.height)
                    print(f'width{width},height {height}')
                    # create pdf canvas
                    c = canvas.Canvas(outputpath,  pagesize=(width, height))  # (612 x 792 pt)


                    # if I ever change the logo I need to update this and the path.
                    logowidth=1622/3.85
                    logoheight=478/3.85

                    websiteurlwidth=2800/6.7
                    websiteurlheight=386/6.7

                    r = 12 / 255
                    g = 72 / 255
                    b = 165 / 255
                    # to actually use colors
                    # c.setFillColor(Color(r, g, b))
                    # Text color
                    if 'dolphin' in savename:
                            rich_navy = Color(0/255, 0/255, 128/255)

                            c.setFillColor(rich_navy)
                            
                    else:
                        c.setFillColor(Color(0, 0, 0))

                    c.setFont("Helvetica-Bold", 67)    

                    maxwidth=width-160
                    # Niiice now it is centered
                    headingtext1 = f"{degreename}"
                    headingtext2="Semester Layout"

                    text_width1 = c.stringWidth(headingtext1, "Helvetica-Bold", 67)
                    if text_width1>maxwidth:
                        font_size = 57
                        c.setFont("Helvetica-Bold", 57)

                        text_width1 = c.stringWidth(headingtext1, "Helvetica-Bold", font_size)
                        if text_width1>maxwidth:
                            c.setFont("Helvetica-Bold", 50)
                            font_size = 50


                            text_width1 = c.stringWidth(headingtext1, "Helvetica-Bold", font_size)



                    x_center1=(width - text_width1) / 2
                    c.drawString(x_center1, height-200, headingtext1)

                    c.setFont("Helvetica-Bold", 67)    

                    text_width2 = c.stringWidth(headingtext2, "Helvetica-Bold", 67)


                    x_center2=(width - text_width2) / 2
                    # No semester layout string I'm good

                    # c.drawString(x_center2, height-257, headingtext2)




                    # create white rectangle in main overlay. 
                   
                    

                    
                    
                    # draw the link path

                    # draw the link as well in the bottom

                    c.save()
                    return width,height
                

                mainoverlaypath=os.path.join(diagram_folder,'mainoverlay.pdf')
                
                createmainoverlaypdf(diagrampath=originaltheme_pdf_file,outputpath=mainoverlaypath)


                print(f'Created mainoverlaypath at {mainoverlaypath}\n ')
                # now just merge them, along with the legend.
                mergedlegendpdf_path='/Users/shalevwiden/Downloads/Coding_Files/Mermaid/Coursemmd/legendfolder/mergedlegend.pdf'

                def merge_diagram_and_overlay_withlegend(pdfpath,mergedlegendpdfpath,mainoverlaypath,outputpath):
                    # well this finally works somewhat
                    diagram_pdf = PdfReader(pdfpath)
                    legendpdf=PdfReader(mergedlegendpdfpath)
                    mainoverlay_pdf = PdfReader(mainoverlaypath)
                    writer = PdfWriter()


                    diagram_page = diagram_pdf.pages[0]
                    mainoverlay_page = mainoverlay_pdf.pages[0]  
                    
                    diagram_page.merge_page(mainoverlay_page)   #  visual merge
                    writer.add_page(diagram_page)

                    legendpage=legendpdf.pages[0]


                    # Add merged page to writer. This line was causing problems but its good to know
                    writer.add_page(legendpage)


                    with open(outputpath, "wb") as finalpdffile:
                        writer.write(finalpdffile)

                        # output path is the final pdf file which will be downloaded

                finaloutputpath=os.path.join(diagram_folder,f'{degreenamecleaned}{savename}.pdf')

                merge_diagram_and_overlay_withlegend(pdfpath=originaltheme_pdf_file,mergedlegendpdfpath=mergedlegendpdf_path, mainoverlaypath=mainoverlaypath,outputpath=finaloutputpath)

                print(f'Created final output path at {finaloutputpath}')



                def delete_unnessary_files():
                    os.remove(originaltheme_pdf_file)
                    os.remove(mainoverlaypath)
                    os.remove(originaltheme_png_file)
                delete_unnessary_files()

                # -----------------MAKE EMPTY NODES HERE
                activateemptynodes=False
                if activateemptynodes:

                    emptynodesfolder=os.path.join(diagram_folder,'emptynodesfolder')
                    if not os.path.exists(emptynodesfolder):
                        os.mkdir(emptynodesfolder) 

                    time.sleep(3)

                    def svg_to_pdf_emptynodes(svg_file, pdf_file):
                        svg2pdf(url=svg_file, write_to=pdf_file)

                    # this should save the empty nodes pdf in the respective folder. Then I'll 
                    # just have to run it through a stylizing function.
                    # This requires you to generate svg functions for every 
                    svg_savefilepath=os.path.join(diagram_folder,f'{degreenamecleaned}-semesterdiagram.svg')

                    empty_nodes_pdffile=os.path.join(emptynodesfolder,f'{degreenamecleaned}-emptynodes.pdf')

                    svg_to_pdf_emptynodes(svg_file=svg_savefilepath,pdf_file=empty_nodes_pdffile)
                    # now run pdf through all the formatting- define functions above.

                    def create_emptynodes_overlaypdf(diagrampath, outputpath):

                        # first get pdf data.
                        base_pdf = PdfReader(diagrampath)
                        page = base_pdf.pages[0]
                        width = float(page.mediabox.width)
                        height = float(page.mediabox.height)
                        print(f'width{width},height {height}')
                        # create pdf canvas
                        c = canvas.Canvas(outputpath,  pagesize=(width, height))  # (612 x 792 pt)


                        # if I ever change the logo I need to update this and the path.
                        logowidth=1622/6
                        logoheight=478/6

                        websiteurlwidth=2800/11
                        websiteurlheight=386/11

                        r = 12 / 255
                        g = 72 / 255
                        b = 165 / 255
                        # to actually use colors
                        # c.setFillColor(Color(r, g, b))
                        # Text color
                        if 'dolphin' in savename:
                            rich_navy = Color(0/255, 0/255, 128/255)

                            c.setFillColor(rich_navy)

                        else:
                            c.setFillColor(Color(0, 0, 0))
                        c.setFont("Helvetica-Bold", 39)    

                        maxwidth=width-90
                        # Niiice now it is centered
                        headingtext1 = f"{degreename}"
                        headingtext2="Semester Layout"

                        text_width1 = c.stringWidth(headingtext1, "Helvetica-Bold", 39)
                        if text_width1>maxwidth:
                            font_size = 35
                            c.setFont("Helvetica-Bold", 35)

                            text_width1 = c.stringWidth(headingtext1, "Helvetica-Bold", font_size)
                            



                        x_center1=(width - text_width1) / 2
                        c.drawString(x_center1, height-75, headingtext1)

                        c.setFont("Helvetica-Bold", 39)    

                        text_width2 = c.stringWidth(headingtext2, "Helvetica-Bold", 39)


                        x_center2=(width - text_width2) / 2
                        # c.drawString(x_center2, height-134, headingtext2)




                        # create white rectangle in main overlay to cover the legend is the thing
                        c.setFillColorRGB(1, 1, 1)  
                        c.rect(0, 0, width, 250, fill=1, stroke=0) 

                        

                        c.drawImage(self.logopath, 25, 9, width=logowidth, height=logoheight)
                        c.drawImage(self.websiteurl_img_path,width-(websiteurlwidth*1.06) , 26, width=websiteurlwidth, height=websiteurlheight)
                        # draw the link path

                        # draw the link as well in the bottom

                        c.save()
                        return width,height
                    

                    emptynodesoverlaypath=os.path.join(emptynodesfolder,'emptynodesoverlay.pdf')
                    if "emptynodesmainoverlay.pdf" not in os.listdir(diagram_folder):
                        create_emptynodes_overlaypdf(diagrampath=empty_nodes_pdffile,outputpath=emptynodesoverlaypath)
                    else:
                        print('\nEmpty nodes overlay was already there so didnt create a new one\n')






                    mergedlegendpdf_path='/Users/shalevwiden/Downloads/Coding_Files/Mermaid/Coursemmd/legendfolder/mergedlegend.pdf'
                    finaloutput_emptynodes_path=os.path.join(emptynodesfolder,f'{degreenamecleaned}-semesterlayout_emptynodes.pdf')

                    merge_diagram_and_overlay_withlegend(pdfpath=empty_nodes_pdffile,mergedlegendpdfpath=mergedlegendpdf_path, mainoverlaypath=emptynodesoverlaypath,outputpath=finaloutput_emptynodes_path)

                    def delete_nodeunnessary_files():
                        # all these are used for the creation of the final pdf
                        os.remove(empty_nodes_pdffile)
                        os.remove(emptynodesoverlaypath)
                        os.remove(svg_savefilepath)

                    delete_nodeunnessary_files()

                    print(f'\nCreated empty nodes final output path at {finaloutput_emptynodes_path}.\n')


            

    def create_oddnumbered_mmd_pdfs(self,savename):

        '''
        This takes the pdfs or svgs created by the above function, and turns them into stylized pdfs.

        Above is where background and node styling can take place.

        Here is where logo, images, sizing, and page appendation can take place.
          -------------------------------------------------
        This one only creates ODD numbered semester pdfs.

        Also to run this you must also run create_mmd_files because this function and the even one delete the pngs after theyre created to save storage.
        '''

        for i in range(1,len(self.schooldata)):

        # in this entire folder we are doing things by degree.


            key=list(self.schooldata)[i]
            degreename=key
            degreename=degreename.replace('/','-').strip()


            degreenamecleaned=degreename.replace(' ','').lower().split('(')
            degreenamecleaned=degreenamecleaned[0]+"-"+degreenamecleaned[-1]
            degreenamecleaned=degreenamecleaned.replace(')','')

            print(f'Starting process for {degreename} mermaid file')
            
            # kept as sugg link as continuity from make_makorcourses_csvs
            sugglink=self.schooldata[key]

            semesterdictionary=getallcourses_splitbysemester(suggcourse_link=sugglink)
            numberofsemesters=len(semesterdictionary)

            if numberofsemesters%2!=0:

            
                # now use this to write to csv files.
                # I can actually finish this fast
                
                degreefolderpath=os.path.join(self.schoolfolderpath,degreename)
                # can change this quite easily
                # theres spaces which isnt great. But theres also spaces in the degreename. 

                diagram_folder=os.path.join(degreefolderpath,'diagrams_and_mmdstuff')
                
                originaltheme_png_file=os.path.join(diagram_folder,f'{degreenamecleaned}-semesterdiagram.png')

                legendonlypng_path='/Users/shalevwiden/Downloads/Coding_Files/Mermaid/Coursemmd/legendfolder/legendonly.png'

                originaltheme_pdf_file=os.path.join(diagram_folder,f'{degreenamecleaned}-semesterdiagram.pdf')


            # step one: convert pdfs to pngs.

                def png_to_pdf(png_path, pdf_path):
                    # Open the PNG and convert to RGB (PDFs can't handle alpha channels)
                    image = Image.open(png_path).convert("RGB")
                    image.save(pdf_path, "PDF")
                    print(f"Saved PDF to: {pdf_path}")
                
                # this is the diagram pdf.
                

                png_to_pdf(png_path=originaltheme_png_file,pdf_path=originaltheme_pdf_file)
                print(f'Created png to pdf for {originaltheme_pdf_file}')


                # This is the legend only pdf. The png is made in seperatelegend.py.

                def createmainoverlaypdf(diagrampath, outputpath):

                    # first get pdf data.
                    base_pdf = PdfReader(diagrampath)
                    page = base_pdf.pages[0]
                    width = float(page.mediabox.width)
                    height = float(page.mediabox.height)
                    print(f'width{width},height {height}')
                    # create pdf canvas
                    c = canvas.Canvas(outputpath,  pagesize=(width, height))  # (612 x 792 pt)


                    # if I ever change the logo I need to update this and the path.
                    logowidth=1622/3.85
                    logoheight=478/3.85

                    websiteurlwidth=2800/6.7
                    websiteurlheight=386/6.7

                    r = 12 / 255
                    g = 72 / 255
                    b = 165 / 255
                    # to actually use colors
                    # c.setFillColor(Color(r, g, b))
                    # Text color
                    
                    # for dolphin:

                    if 'dolphin' in savename:
                        rich_navy = Color(0/255, 0/255, 128/255)

                        c.setFillColor(rich_navy)
                    else:
                        c.setFillColor(Color(0, 0, 0))



                    c.setFont("Helvetica-Bold", 67)    

                    maxwidth=width*.6
                    
                    headingtext1 = f"{degreename.split('(')[0]}"
                    headingtext2 = f"({degreename.split('(')[1]}"

                    headingtext3="Semester Layout"

                    # text_width1 = c.stringWidth(headingtext1, "Helvetica-Bold", 67)
                    # if text_width1>maxwidth:
                    #     font_size = 57
                    #     c.setFont("Helvetica-Bold", 57)

                    #     text_width1 = c.stringWidth(headingtext1, "Helvetica-Bold", font_size)
                    #     if text_width1>maxwidth:
                    #         c.setFont("Helvetica-Bold", 50)
                    #         font_size = 50


                    #         text_width1 = c.stringWidth(headingtext1, "Helvetica-Bold", font_size)



                    
                    x_position1=(190)
                    c.drawString(x_position1, height-455, headingtext1)


                    text_width2 = c.stringWidth(headingtext2, "Helvetica-Bold", 67)


                    x_position2=(190)
                    c.drawString(x_position2, height-550, headingtext2)

                    # heading text 2 will always be 67, "Semester Layout"
                    c.setFont("Helvetica-Bold", 67)

                    x_position3=(190)
                    # c.drawString(x_position3, height-645, headingtext3)




                    # create white rectangle in main overlay. 
                   

                    

                    # draw the link as well in the bottom

                    c.save()
                    return width,height
                

                mainoverlaypath=os.path.join(diagram_folder,'mainoverlay.pdf')
                
                createmainoverlaypdf(diagrampath=originaltheme_pdf_file,outputpath=mainoverlaypath)


                print(f'Created mainoverlaypath at {mainoverlaypath}\n ')
                # now just merge them, along with the legend.
                mergedlegendpdf_path='/Users/shalevwiden/Downloads/Coding_Files/Mermaid/Coursemmd/legendfolder/mergedlegend.pdf'

                def merge_diagram_and_overlay_withlegend(pdfpath,mergedlegendpdfpath,mainoverlaypath,outputpath):
                    # well this finally works somewhat
                    diagram_pdf = PdfReader(pdfpath)
                    legendpdf=PdfReader(mergedlegendpdfpath)
                    mainoverlay_pdf = PdfReader(mainoverlaypath)
                    writer = PdfWriter()


                    diagram_page = diagram_pdf.pages[0]
                    mainoverlay_page = mainoverlay_pdf.pages[0]  
                    
                    diagram_page.merge_page(mainoverlay_page)   #  visual merge
                    writer.add_page(diagram_page)

                    legendpage=legendpdf.pages[0]


                    # Add merged page to writer. This line was causing problems but its good to know
                    writer.add_page(legendpage)


                    with open(outputpath, "wb") as finalpdffile:
                        writer.write(finalpdffile)

                        # output path is the final pdf file which will be downloaded

                finaloutputpath=os.path.join(diagram_folder,f'{degreenamecleaned}{savename}.pdf')

                merge_diagram_and_overlay_withlegend(pdfpath=originaltheme_pdf_file,mergedlegendpdfpath=mergedlegendpdf_path, mainoverlaypath=mainoverlaypath,outputpath=finaloutputpath)

                print(f'Created final output path at {finaloutputpath}')



                def delete_unnessary_files():
                    os.remove(originaltheme_pdf_file)
                    os.remove(mainoverlaypath)
                    os.remove(originaltheme_png_file)
                delete_unnessary_files()

                # -----------------MAKE EMPTY NODES HERE
                activateemptynodes=False
                if activateemptynodes:

                    emptynodesfolder=os.path.join(diagram_folder,'emptynodesfolder')
                    if not os.path.exists(emptynodesfolder):
                        os.mkdir(emptynodesfolder) 

                    time.sleep(3)

                    def svg_to_pdf_emptynodes(svg_file, pdf_file):
                        svg2pdf(url=svg_file, write_to=pdf_file)

                    # this should save the empty nodes pdf in the respective folder. Then I'll 
                    # just have to run it through a stylizing function.
                    # This requires you to generate svg functions for every 
                    svg_savefilepath=os.path.join(diagram_folder,f'{degreenamecleaned}-semesterdiagram.svg')

                    empty_nodes_pdffile=os.path.join(emptynodesfolder,f'{degreenamecleaned}-emptynodes.pdf')

                    svg_to_pdf_emptynodes(svg_file=svg_savefilepath,pdf_file=empty_nodes_pdffile)
                    # now run pdf through all the formatting- define functions above.

                    def create_emptynodes_overlaypdf(diagrampath, outputpath):

                        # first get pdf data.
                        base_pdf = PdfReader(diagrampath)
                        page = base_pdf.pages[0]
                        width = float(page.mediabox.width)
                        height = float(page.mediabox.height)
                        print(f'width{width},height {height}')
                        # create pdf canvas
                        c = canvas.Canvas(outputpath,  pagesize=(width, height))  # (612 x 792 pt)


                        # if I ever change the logo I need to update this and the path.
                        logowidth=1622/6
                        logoheight=478/6

                        websiteurlwidth=2800/11
                        websiteurlheight=386/11

                        r = 12 / 255
                        g = 72 / 255
                        b = 165 / 255
                        # to actually use colors
                        # c.setFillColor(Color(r, g, b))
                        # Text color
                        c.setFillColor(Color(0, 0, 0))

                        c.setFont("Helvetica-Bold", 39)    

                        maxwidth=width*.45
                        # Niiice now it is centered
                            
                        headingtext1 = f"{degreename.split('(')[0]}"
                        headingtext2 = f"({degreename.split('(')[1]}"

                        headingtext3="Semester Layout"

                        # smaller font since the svg is alot smaller
                        text_width1 = c.stringWidth(headingtext1, "Helvetica-Bold", 39)
                        if text_width1>maxwidth:
                            font_size = 35
                            c.setFont("Helvetica-Bold", 35)

                            text_width1 = c.stringWidth(headingtext1, "Helvetica-Bold", font_size)
                            


# --------------------------------------------

                        x_position1=(150)
                        c.drawString(x_position1, height-230, headingtext1)

                        c.setFont("Helvetica-Bold", 39)    

                        text_width2 = c.stringWidth(headingtext2, "Helvetica-Bold", 39)


                        x_position2=(150)
                        c.drawString(x_position2, height-290, headingtext2)



                        x_position3=(150)
                        # c.drawString(x_position3, height-350, headingtext3)


                        # create white rectangle in main overlay to cover the legend is the thing
                        c.setFillColorRGB(1, 1, 1)  
                        c.rect(0, 0, width, 250, fill=1, stroke=0) 

                        

                        c.drawImage(self.logopath, 25, 9, width=logowidth, height=logoheight)
                        c.drawImage(self.websiteurl_img_path,width-(websiteurlwidth*1.06) , 26, width=websiteurlwidth, height=websiteurlheight)
                        # draw the link path

                        # draw the link as well in the bottom

                        c.save()
                        return width,height
                    

                    emptynodesoverlaypath=os.path.join(emptynodesfolder,'emptynodesoverlay.pdf')
                    if "emptynodesmainoverlay.pdf" not in os.listdir(diagram_folder):
                        create_emptynodes_overlaypdf(diagrampath=empty_nodes_pdffile,outputpath=emptynodesoverlaypath)
                    else:
                        print('\nEmpty nodes overlay was already there so didnt create a new one\n')






                    mergedlegendpdf_path='/Users/shalevwiden/Downloads/Coding_Files/Mermaid/Coursemmd/legendfolder/mergedlegend.pdf'
                    finaloutput_emptynodes_path=os.path.join(emptynodesfolder,f'{degreenamecleaned}-semesterlayout_emptynodes.pdf')

                    merge_diagram_and_overlay_withlegend(pdfpath=empty_nodes_pdffile,mergedlegendpdfpath=mergedlegendpdf_path, mainoverlaypath=emptynodesoverlaypath,outputpath=finaloutput_emptynodes_path)

                    def delete_nodeunnessary_files():
                        # all these are used for the creation of the final pdf
                        os.remove(empty_nodes_pdffile)
                        os.remove(emptynodesoverlaypath)
                        os.remove(svg_savefilepath)

                    delete_nodeunnessary_files()

                    print(f'\nCreated empty nodes final output path at {finaloutput_emptynodes_path}.\n')



# archdata testing
def archtesting():
    archdata=theasset[0]

    archschoolkey=list(archdata)[0]
    archschoolname=archdata[archschoolkey]
    # print(f'School key: {archschoolkey}. School name: {archschoolname}')

    architecturefiles=makeSemesterFiles(schooldata=archdata)
    print('Testing:\nArchitecture School Folder Path')
    print(architecturefiles.schoolfolderpath)
    print('Testing:\nArchitecture School Name')

    print('Getting the attribute:\n')
    print(getattr(architecturefiles,'schoolname'))
    print()

    # architecturefiles.make_mermaid_files()
    # architecturefiles.create_mmd_pdfs(savename='-tystare')
    # architecturefiles.create_oddnumbered_mmd_pdfs('-tystare')



    architecturefiles.make_mermaid_files()
    architecturefiles.create_mmd_pdfs(savename='-tystare')
    architecturefiles.create_oddnumbered_mmd_pdfs(savename='-tystare')

    dolphin=False
    if dolphin:

        architecturefiles.make_mermaid_files()
        architecturefiles.create_mmd_pdfs(savename='-dolphinocean')
        architecturefiles.create_oddnumbered_mmd_pdfs('-dolphinocean')

archtesting()




def unpacktheasset_into_makefilesclass(theasset):
    '''
    This is the primary function that works with the functions in the class to make files
    '''
    
    for schooldict in theasset:
        schoolobject=makeSemesterFiles(schooldata=schooldict)
        schoolobject.upload_to_database()   
       
    


def runentirefile(theasset):

    for schooldict in theasset:
        schoolobject=makeSemesterFiles(schooldata=schooldict)
        



        schoolobject.make_mermaid_files()
        schoolobject.create_mmd_pdfs(savename='-tystare')
        schoolobject.create_oddnumbered_mmd_pdfs(savename='-tystare')

        dolphin=False
        if dolphin:

            schoolobject.make_mermaid_files()
            schoolobject.create_mmd_pdfs(savename='-dolphinocean')
            schoolobject.create_oddnumbered_mmd_pdfs(savename='-dolphinocean')

runentirefile(theasset=theasset)