import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os

import csv
import openpyxl



from openpyxl import load_workbook
from openpyxl import Workbook
# use this to define the function define_start_column
from openpyxl.utils import column_index_from_string

# this assigns cells colors
from openpyxl.styles import PatternFill


import os

from openpyxl.styles import Font
from openpyxl.styles import Border, Side, Alignment

# good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'the version of openpyxl is\n {(openpyxl.__version__)}')

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
            print(f'\ncsv object has been rest to {len(csvobjectdict)}\n\n\n')
            
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

                writer.writerow(['','','',f'Total Hours: {totalhours}',''])
                writer.writerow(['DegreeView','','','','','DegreeView'])

                # this is for those giant architecture majors and some engineering that take like 6 years
        

                



        

        print(f'Made a semestercsv for {degreename}:\n As {semestercsvfilename}')
#-----------------------------------------------------------------------------------

    def make_horizontal_csvfiles(self):
         '''for each degree in school data make a csv thats horizontal with 4 semesters on each side.'''

         ''' Only works for degrees with 8 semesters. 
         
         Just test this with say archdata and see if it works
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
            
            degreefolderpath=os.path.join(self.schoolfilepath,degreename)
            # can change this quite easily
            semestercsvfilename=os.path.join(degreefolderpath,f'{degreename} semestercsvfile.csv')

            totalhours=0
            numberofsemesters=len(semesterdictionary)
            csvobjectdict={}                        
            print(f'csv object has been rest to {len(csvobjectdict)}\n\n\n\n\n\n\n')
            '''
            Use this rowcount way to then go back and use the same indexes for the horizontal side is the thing haha. 
            '''
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

                    writer.writerow(['','','',f'Total Hours: {totalhours}','',''])
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
            degreename=degreename.replace('/','-').strip()

            print(f'Starting process for {degreename} excel file')
            
            # kept as sugg link as continuity from make_makorcourses_csvs
            sugglink=self.schooldata[key]

            
            semesterdictionary=getallcourses_splitbysemester(suggcourse_link=sugglink)
            # now use this to write to csv files.
            # I can actually finish this fast
            
            degreefolderpath=os.path.join(self.schoolfilepath,degreename)
            # can change this quite easily
            # theres spaces which isnt great. But theres also spaces in the degreename. 
            semeseter_excel_filename=os.path.join(degreefolderpath,f'{degreename} semesterfile.xlsx')

            totalhours=0
            numberofsemesters=len(semesterdictionary)
            excelobject=[]                        
            print(f'Excel object has been reset to {len(excelobject)}\n\n\n')



            '''
            Use Font and OpenPyXL to create nicely formatted tabular data
            '''

            semesterworkbook=Workbook()
            # gets the default worksheet
            ws=semesterworkbook.active



                
            titlefont=Font(size=24,bold=True)

            headingborder=Border(bottom=Side(style='mediumDashDot'))

            headingsfonts=Font(size=18,bold=True)
            subheadingsfont=Font(size=16,bold=True)
            utnamefont=Font(size=20, color='FFBF5701', name='Georgia',bold=True)
            # update later
            semesterfont=Font(bold=True,size=16)

            datafont=Font(size=15,name='Helvetica',underline='single')


            leftalign=Alignment(horizontal='left')
            centeralign=Alignment(horizontal='center')
            



            # total height of 40


            # first row after title that is. Start at row 3 since rows 1 and 2 were merged
            firstrow=[f'{degreename}',"","","",f'{self.schoolname}',"The University of Texas at Austin"]
                
            # colindex is like i            
            # start= 1 means start at the first column
            for col_index, value in enumerate(firstrow, start=1):
                # adjust row here
                headingcell=ws.cell(row=3, column=col_index, value=value)
                # use.font to assign the font I see
                if col_index==6:

                    headingcell.font=utnamefont
                    headingcell.border=headingborder
                else:
                    headingcell.font=headingsfonts
                    headingcell.border=headingborder

                    # print(datacell.font.size)


            blankrow=['','','','','','','','']
            # appends to the next empty row. Like writer.writerow(['']) for csvs
            ws.append(blankrow)
            
                        
            thirdrow=['','Course Code','Course Name','Hours','Category','Upper/Lower Division']
            ws.append(thirdrow)
            # now apply styles
            for cell in ws[5]:
                cell.font=subheadingsfont


            # now the meat of the file, the data
            



            # for each semester
            rowcount=0
            for semesternum in range(numberofsemesters):
                semester=list(semesterdictionary)[semesternum]
                # semester courses is a dictionary of its own as well
                semestercourses=semesterdictionary[semester]
                # that means the semester will be on the first row
                excelobject.append([f'{semester}'])
                rowcount+=1
                for coursenameindex in range(len(semestercourses)):

                    coursename=list(semestercourses)[coursenameindex]
                    # if its NOT a list of lists, ie, a normal course entry
                    if len(semestercourses[coursename])==4 and not isinstance(semestercourses[coursename][0],list):
                        coursecode, coursehours, upperdivstatus, coursecategory=semestercourses[coursename]
                        excelobject.append(["",coursecode,coursename,coursehours,coursecategory,upperdivstatus])
                        rowcount+=1
                        if coursehours!='':
                            totalhours+=int(coursehours)
                    
                    else:
                        listofcourses=semestercourses[coursename]
                        for i in range(len(listofcourses)):
                            coursecode, coursehours, upperdivstatus, coursecategory=listofcourses[i]
                            excelobject.append(["",coursecode,coursename,coursehours,coursecategory,upperdivstatus])
                            rowcount+=1

                            if coursehours!='':
                                totalhours+=int(coursehours)


                # line between semesters
                excelobject.append(['','','','',''])
                rowcount+=1

            # adding to excel file
            # rowval is important for adding rows in order
            rowval=6

            for rowentry in range(len(excelobject)):
                # update it here so it updates by row not column...although
                rowval += 1
                        # start at column one, and then remember the padding rows are added later. 
                for col_index, value in enumerate(excelobject[rowentry], start=1):
                    # change alignnment here. 1 indexed not 0
                    datacell = ws.cell(row=rowval, column=col_index, value=value)

                    if col_index==1:
                        # use.font to assign the font I see
                        datacell.font=semesterfont
                        datacell.alignment=centeralign
                    elif col_index in [2,3]:
                        datacell.font=datafont
                        datacell.alignment=leftalign
                    elif col_index==4: #hourscol
                        datacell.font=datafont
                        datacell.alignment=centeralign
                    elif col_index in [5,6]:
                        datacell.font=datafont
                        datacell.alignment=leftalign
                    
            
                       


            print(f'Excel object for {degreename}:\n{excelobject}')
            print(f'len excel object={len(excelobject)}')
            

# -----------------------------end data stuff --------------------------------------------------------
            ws.append(blankrow)
            totalhoursrow=['','','',f'Total Hours: {totalhours}','','']

            lastrowindex=rowcount+6
            for col_index, value in enumerate(totalhoursrow, start=1):
                
                # use.font to assign the font I see
                cell=ws.cell(row=lastrowindex, column=col_index, value=value)
                # FF=full opacity 
                cell.font=datafont

           
            lastrow=['DegreeView','','','','','DegreeView']
            lastrowindex+=2 # 6 rows before we start data stuff. Then rowcount is the amount of data. 

            for col_index, value in enumerate(lastrow, start=1):
                
                # use.font to assign the font I see
                lastcell=ws.cell(row=lastrowindex, column=col_index, value=value)
                # FF=full opacity 
                lastcell.font=Font(size=18, bold=True, color='FF005f76')
                lastcell.alignment=Alignment(textRotation=161)




            # ---------------formatting stuff------------------
            
            # add padding
            
            
            ws.insert_rows(1)      #new row
            ws.insert_cols(1)       # new col

            # ws.columns gets columns. Each column is a tuple of cells
            for column_cells in ws.columns:
                # max function gets the max in a list. Same for min
                # generator must be in ()
                cellwidthgenerator=(len(str(cell.value)) if cell.value else 0 for cell in column_cells)
                colwidth = max(cellwidthgenerator)

                firstcell=column_cells[0]
                # every cell has a .column_letter attribute
                col_letter = firstcell.column_letter
                col_index=column_index_from_string(col_letter)
                # scale the width factor
                if col_index==7:  
                    # make the UT Austin column alot wider
                    ws.column_dimensions[col_letter].width = int(colwidth)*2
                elif col_index==6:
                    ws.column_dimensions[col_letter].width = int(colwidth)*1.4
                elif col_index==5:
                    ws.column_dimensions[col_letter].width=int(colwidth)*.7

                # the semester column
                elif col_index==2:
                    ws.column_dimensions[col_letter].width=int(colwidth)*.7
            

                else:
                    ws.column_dimensions[col_letter].width = int(colwidth)*1.2
                



            # set sizes for the padding row and column. Units of default font which is usually Arial it seems

            ws.column_dimensions['A'].width=15
            ws.column_dimensions['H'].width=15
            ws.row_dimensions[1].height=25
            ws.row_dimensions[lastrowindex+2].height=25

            # ------------------------------------TITLE STUFF-------------------------------------------

            # create a merged 'Degree view and degreename header can't lie".
            ws.merge_cells('B2:G3')    
            ws.row_dimensions[2].height = 30
            ws.row_dimensions[3].height = 30
            mergedrowcontent=f'{degreename} Sample Semester Layout'
            
            # refer to top left of merged cells
            titlecell=ws['B2']
            titlecell.value=mergedrowcontent
            titlecell.alignment = Alignment(horizontal='center', vertical='center')
            titlecell.font=titlefont

        # ------------------------ CONTINUE FORMATTING STUFF -----------------------------------------------------
            # apply a border around the entire file -----------------------------------------------------------------------------

            # make it responsive based on the amount of data
            # remove the +1 here to have no border
            rows = list(ws['B2':f'G{lastrowindex+1}'])
            min_row = 2
            max_row = lastrowindex+1

            min_col = column_index_from_string('B')  
            max_col = column_index_from_string('G') 

            

            
            # this is the border that will go around everything
            entire_ws_border=Side(style='thick',color='000000')
            
            for row_index, row in enumerate(rows, start=min_row):
                for col_index, cell in enumerate(row, start=min_col):
                    
                    # remember we defined side. and you do Border(Side=style))
                    '''
                    This is the final peice of the puzzle that adds borders.
                    If sides if empty, then
                    cell.border = Border(), which defines no borders. Normally it will be entire_ws_border border preset. 
                    '''
                    cell.border = Border(
                    top=entire_ws_border if row_index == min_row else None,
                    bottom=entire_ws_border if row_index == max_row else None,
                    left=entire_ws_border if col_index == min_col else None,
                    right=entire_ws_border if col_index == max_col else None,
                )
            
            # make the entire worksheet a color:
            backgroundcolor=PatternFill(fill_type="solid", start_color="F0F0F0") #end_color='0000FF' fill_type="gray125" or linear later

            # have the background be like a padding. 
            for row in ws.iter_rows(min_row=1, max_row=lastrowindex+2, min_col=1, max_col=8):
                for cell in row:
                    cell.fill = backgroundcolor
            
            # reverse the background for cells with content:

            whitefill=PatternFill(fill_type="solid", start_color="FFFFFF")
            # re-add gridline borders:

            gridline_border = Border(
                left=Side(border_style="thin", color="DDDDDD"),
                right=Side(border_style="thin", color="DDDDDD"),
                top=Side(border_style="thin", color="DDDDDD"),
                bottom=Side(border_style="thin", color="DDDDDD")
            )

            for row in ws.iter_rows(min_row=min_row, max_row=max_row, min_col=min_col, max_col=max_col):
                for cell in row:
                    cell.fill = whitefill
                    cell.border=gridline_border
                    
            
            degreeviewpath='/Users/shalevwiden/Downloads/Projects/degreeview'
            semesterworkbook.save(semeseter_excel_filename)
            print(f'Saved workbook at {os.path.abspath(semeseter_excel_filename)}')


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

architecturefiles.make_excel_files()

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