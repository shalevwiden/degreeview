import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os

print(f'the version of beautiful soup is\n {(bs4.__version__)}')
print(f'the version of requests is\n {(requests.__version__)}')
print(f'\nthe python version being used is:{sys.executable}\n')

print('\xa0')

'''
This document consists of all the trial and error, playing around, and testing I had to do throughout this project to get the code right.
'''

# practice list comprehensions

testlist=[1,2]
print(testlist)
# wow can reassign a list to a list thats crazy
testlist=testlist[0]
print(testlist)
list1=list(range(20))

# what is .issubset?
testlink="https://catalog.utexas.edu/undergraduate/engineering/degrees-and-programs/"
splitlink=testlink.split('/')
print(splitlink)
reconstructedlink=''
reconstructedlink+=f'{splitlink[0]}//{splitlink[2]}/{splitlink[3]}/{splitlink[4]}/'
print(reconstructedlink)

print()

# get a certain element in a dict without knowing the key
testdict={'a':1,'b':2,'c':3}

for i in testdict:
    print(i)
    print('Should print the keys')
firstkey=list(testdict)[0]
firstvalue=testdict[firstkey]

# Hell yeah
print(firstkey)
print(firstvalue)
print(testdict.keys())

# get upper divison status
archlist=['ARC 318L','ARC 334K','ARC 308','PHY 105M',"Upper-division BAX courses (Major)"]

resultdict={}
lowerdivstatus="Lower Division"
upperdivstatus="Upper Division"
for i in archlist:
    
    if any(char.isdigit() for char in i):
        coursenum=i.split(' ')[-1][1:3]
        print(coursenum)
        if int(coursenum)>=20:
             
            resultdict[i]=upperdivstatus
        else:
            resultdict[i]=lowerdivstatus


    else:
        if "upper" in i.lower():
            resultdict[i]=upperdivstatus
        else:
            resultdict[i]=lowerdivstatus
print(resultdict)



# i gotta append carefully to make sure everything lines up

# listofliststesting
listoflists=[]
for i in range(5):
    innerlist=[]
    for i in range(3):
        innerlist.append(i+1)
    listoflists.append(innerlist)
print(f'listoflists{listoflists}')
print(len(listoflists))

# removelist=[]
# for i in range(20):
#     removelist.append(i)    
# for i in range(len(removelist)):
#     if (i+1)%4==0:
#         del removelist[i]
# print(f'Remove list{removelist}')

print('tr trickiness\n')
unfilteredtrs=[[1,2,3],[1,2,3],[1,2,4]]
trs=[]
for tr in unfilteredtrs:
    if 4 not in tr:
        trs.append(tr)

# use all keyword
print(f'trs:{trs}')

testall3=['yo','mama','has','letters','in','her','name','longword']
print('\nList comprehensions mf\n')

testall3list=[word for word in testall3 if len(word)>4]
print(testall3list)

# how to make a jupyter cell - type # %%

# study up on that later


# all learning
# %%
testall2=[5,10,15,20]

print('Are all nums above 10?:')
print(all(n>10 for n in testall2))
print('\n')
print('All nums above 3' if all(n>3 for n in testall2) else 'They are below')


# any learning
# %%
testlist1=[1,2,3,4,5,4,3,2,1]
numvar=6
print('yes' if any(num==numvar for num in testlist1) else f'{numvar} not in testlist1')


#%% 
print('testmf')
# I love abspath
print(os.path.abspath('degreeview'))
degreeviewfolderpath=os.path.abspath('degreeview')
archname='School of Architecture'
filepath=os.path.join(degreeviewfolderpath,archname)

print(f'Filepath: {filepath}\n')
print(type(filepath))


# %%


# this bit of logic processes the degree heading from the suggested arrangement of courses tab
# particularly the ones that have more than one comma
# %%
degreename='Suggested Arrangement of Courses, Speech, Language, and Hearing Sciences (BSSLH)'
suggheading,restofdegreename=degreename.split(',')[0], degreename.split(',')[1:]
degreename=''
for i in range(len(restofdegreename)):
    if i==-1:
        degreename+=restofdegreename[i]
    else:
        degreename+=f'{restofdegreename[i]},'
    
print(degreename)

# %%
print('\nBack to normal python')

# %%
keysdict={'firstkey': 25,'secondkey':30}
print(keysdict.keys())
print(len(keysdict.keys()))
print(len(keysdict))
# %%

a,b,c=[5,6,7]
print(a,b,c)
# %%


#%%
import requests
import bs4
from bs4 import BeautifulSoup


geophysics_suggpage=requests.get('https://catalog.utexas.edu/undergraduate/geosciences/degrees-and-programs/bs-geological-sciences/sugg-geophysics-bsgeosci/')
geosoup=BeautifulSoup(geophysics_suggpage.text,'html.parser')


'''The following code is very helpful to understand what the heck is going on with the & stuff. 

Turns out the coursecode stuff was modified more simply, but the coursename stuff was needed.

'''
tr='''<tr class="odd"><td class="codecol"><a href="/search/?P=PHY%20301" title="PHY&nbsp;301" class="bubblelink code" onclick="return showCourse(this, 'PHY 301');">PHY&nbsp;301</a><br><span style="margin-left:20px;" class="blockindent">&amp;&nbsp;<a href="/search/?P=PHY%20101L" title="PHY&nbsp;101L" class="bubblelink code" onclick="return showCourse(this, 'PHY 101L');">PHY&nbsp;101L</a></span></td><td>Mechanics<br><span style="margin-left:20px;" class="blockindent">and Laboratory for Physics 301</span> (General Education)</td><td class="hourscol">4</td></tr>'''
falsetr='''<tr class="even"><td class="codecol"><a href="/search/?P=CH%20302" title="CH&nbsp;302" class="bubblelink code" onclick="return showCourse(this, 'CH 302');">CH&nbsp;302</a></td><td>Principles of Chemistry II (Core) <sup>030</sup></td><td class="hourscol">3</td></tr>'''
trsoup=BeautifulSoup(tr,'html.parser')
tds=trsoup.find_all('td')

coursecode=tds[0]

# is this logic good? Idk but we should check
coursename=tds[1]
nameblock=coursename.find('span',class_="blockindent")
codeblock=coursecode.find('span',class_="blockindent")

coursecode=tds[0].get_text()
originalcoursecode=coursecode
coursename=tds[1].get_text()    


if nameblock:   
    coursename=coursename.split('and')

    fullname=''
    for i in range(len(coursename)):
        if i==len(coursename)-1:
            fullname+=coursename[i].strip()

        else:
            fullname+=coursename[i].strip()+' and '

    
if codeblock:
    print(f'\nCodeblock found:\n{codeblock}')
    print(f'Codeblock text:\n{codeblock.get_text()}\n')


    coursecode=coursecode.split('&')
    fullcode=''
    for i in range(len(coursecode)):
        if i==len(coursecode)-1:
            fullcode+=coursecode[i].strip()

        else:
            fullcode+=coursecode[i].strip()+' & '
else:
    print('No codeblock')


# two ands in this mf
coursename='Wave Motion and Optics and Laboratory for Physics 315 (General Education)'

print(f'Original coursecode {originalcoursecode}')




print('fullname')
print(fullname)
print('\n\nfullcode\n')
print(fullcode)

# %%
maxlist=list(range(10,50))
print(max(maxlist))
print(min(maxlist))
# %%

#%% 
#triangular growth sequence

newval=0
for i in range(1,10):
    newval+=i
    print(newval)
# %%

# %%
# openpyxl stuff
#  sides = {}
# # loop through all rows and see if it matches this criteria
# if row_index == min_row:
#     sides['top'] = entire_ws_border
# if row_index == max_row:
#     sides['bottom'] = entire_ws_border
# if col_index == min_col:
#     sides['left'] = entire_ws_border
# if col_index == max_col:
#     sides['right'] = entire_ws_border

# # remember we defined side. and you do Border(Side=style))
# # dictionary unpacking
# '''
# This is the final peice of the puzzle that adds borders.
# sides dict for every cell. If sides if empty, then
# cell.border = Border(), which defines no borders
# '''
# cell.border = Border(**sides)

#%%
degreelist=["schoolofarchitecture/interiordesign-bsid-rendered-csv.html","schoolofarchitecture/architecture-barch-rendered-csv.html","schoolofarchitecture/architecture-architecturalengineering-barch-bsarche-rendered-csv.html","schoolofarchitecture/architecture-planiihonors-barch-ba-rendered-csv.html","schoolofarchitecture/architecturalstudies-bsas-rendered-csv.html","redmccombsschoolofbusiness/accounting-bba-rendered-csv.html","redmccombsschoolofbusiness/businessanalytics-bba-rendered-csv.html","redmccombsschoolofbusiness/businessadministration,honorstrack-bba-rendered-csv.html","redmccombsschoolofbusiness/finance-bba-rendered-csv.html","redmccombsschoolofbusiness/internationalbusiness-bba-rendered-csv.html","redmccombsschoolofbusiness/management-bba-rendered-csv.html","redmccombsschoolofbusiness/managementinformationsystems-bba-rendered-csv.html","redmccombsschoolofbusiness/marketing-bba-rendered-csv.html","redmccombsschoolofbusiness/supplychainmanagement-bba-rendered-csv.html","schoolofcivicleadership/civicshonors-ba-rendered-csv.html","moodycollegeofcommunication/advertising-bsadv-rendered-csv.html","moodycollegeofcommunication/communicationandleadership-bscomm&lead-rendered-csv.html","moodycollegeofcommunication/communicationstudies-bscommstds-rendered-csv.html","moodycollegeofcommunication/journalism-bj-rendered-csv.html","moodycollegeofcommunication/publicrelations-bspr-rendered-csv.html","moodycollegeofcommunication/radio-television-film-bsrtf-rendered-csv.html","moodycollegeofcommunication/speech,language,andhearingsciences-bsslh-rendered-csv.html","collegeofeducation/athletictraining-bsathtrng-rendered-csv.html","collegeofeducation/education-bsed-rendered-csv.html","collegeofeducation/youthandcommunitystudies-bsed-rendered-csv.html","collegeofeducation/appliedmovementscience-bskin&health-rendered-csv.html","collegeofeducation/exercisescience-bskin&health-rendered-csv.html","collegeofeducation/healthpromotionandbehavioralscience-bskin&health-rendered-csv.html","collegeofeducation/physicalcultureandsportsstudies-bskin&health-rendered-csv.html","collegeofeducation/sportmanagement-bskin&health-rendered-csv.html","cockrellschoolofengineering/aerospaceengineering-bsase-rendered-csv.html","cockrellschoolofengineering/architecturalengineering-bsarche-rendered-csv.html","cockrellschoolofengineering/biomedicalengineering-bsbiomede-rendered-csv.html","cockrellschoolofengineering/chemicalengineering-bsche-rendered-csv.html","cockrellschoolofengineering/civilengineering-bsce-rendered-csv.html","cockrellschoolofengineering/computationalengineering-bscompe-rendered-csv.html","cockrellschoolofengineering/electricalandcomputerengineering-bsece-rendered-csv.html","cockrellschoolofengineering/environmentalengineering-bsenve-rendered-csv.html","cockrellschoolofengineering/geosystemsengineering-bsge-rendered-csv.html","cockrellschoolofengineering/mechanicalengineering-bsme-rendered-csv.html","cockrellschoolofengineering/petroleumengineering-bspe-rendered-csv.html","collegeoffinearts/acting-bfa-rendered-csv.html","collegeoffinearts/arteducation-bfa-rendered-csv.html","collegeoffinearts/dance-bfa-rendered-csv.html","collegeoffinearts/design-bfa-rendered-csv.html","collegeoffinearts/studioart-bfa-rendered-csv.html","collegeoffinearts/theatreeducation-bfa-rendered-csv.html","collegeoffinearts/composition-bmusic-rendered-csv.html","collegeoffinearts/jazz-bmusic-rendered-csv.html","collegeoffinearts/musicperformance-bmusic-rendered-csv.html","collegeoffinearts/musicstudies-bmusic-rendered-csv.html","collegeoffinearts/arthistory-ba-rendered-csv.html","collegeoffinearts/design-ba-rendered-csv.html","collegeoffinearts/studioart-ba-rendered-csv.html","collegeoffinearts/theatreanddance-batd-rendered-csv.html","collegeoffinearts/music-bamusic-rendered-csv.html","collegeoffinearts/artsandentertainmenttechnologies-bsaet-rendered-csv.html","johna.andkatherineg.jacksonschoolofgeosciences/geosciences-bags-rendered-csv.html","johna.andkatherineg.jacksonschoolofgeosciences/geosciences-bsenvirsci-rendered-csv.html","johna.andkatherineg.jacksonschoolofgeosciences/climatesystemscience-bsgs-rendered-csv.html","johna.andkatherineg.jacksonschoolofgeosciences/generalgeology-bsgs-rendered-csv.html","johna.andkatherineg.jacksonschoolofgeosciences/geophysics-bsgs-rendered-csv.html","johna.andkatherineg.jacksonschoolofgeosciences/geosciences-bsgs-rendered-csv.html","johna.andkatherineg.jacksonschoolofgeosciences/hydrologyandwaterresources-bsgs-rendered-csv.html","johna.andkatherineg.jacksonschoolofgeosciences/geosystemsengineering-bsge-rendered-csv.html","schoolofinformation/informatics-ba-rendered-csv.html","schoolofinformation/informatics-bsi-rendered-csv.html","collegeofliberalarts/africanandafricandiasporastudies-ba-rendered-csv.html","collegeofliberalarts/americanstudies-ba-rendered-csv.html","collegeofliberalarts/anthropology-ba-rendered-csv.html","collegeofliberalarts/asianculturesandlanguages-ba-rendered-csv.html","collegeofliberalarts/asianstudies-ba-rendered-csv.html","collegeofliberalarts/classicallanguages-ba-rendered-csv.html","collegeofliberalarts/classicalstudies-ba-rendered-csv.html","collegeofliberalarts/economics-ba-rendered-csv.html","collegeofliberalarts/english-ba-rendered-csv.html","collegeofliberalarts/ethnicstudies-ba-rendered-csv.html","collegeofliberalarts/europeanstudies-ba-rendered-csv.html","collegeofliberalarts/frenchstudies-ba-rendered-csv.html","collegeofliberalarts/geography-ba-rendered-csv.html","collegeofliberalarts/german-ba-rendered-csv.html","collegeofliberalarts/government-ba-rendered-csv.html","collegeofliberalarts/healthandsociety-ba-rendered-csv.html","collegeofliberalarts/history-ba-rendered-csv.html","collegeofliberalarts/humandimensionsoforganizations-ba-rendered-csv.html","collegeofliberalarts/humanities-ba-rendered-csv.html","collegeofliberalarts/internationalrelationsandglobalstudies-ba-rendered-csv.html","collegeofliberalarts/italianstudies-ba-rendered-csv.html","collegeofliberalarts/jewishstudies-ba-rendered-csv.html","collegeofliberalarts/latinamericanstudies-ba-rendered-csv.html","collegeofliberalarts/linguistics-ba-rendered-csv.html","collegeofliberalarts/mexicanamericanandlatina-ostudies-ba-rendered-csv.html","collegeofliberalarts/middleeasternstudies-ba-rendered-csv.html","collegeofliberalarts/philosophy-ba-rendered-csv.html","collegeofliberalarts/psychology-ba-rendered-csv.html","collegeofliberalarts/race,indigeneity,andmigration-ba-rendered-csv.html","collegeofliberalarts/religiousstudies-ba-rendered-csv.html","collegeofliberalarts/rhetoricandwriting-ba-rendered-csv.html","collegeofliberalarts/russian,easteuropean,andeurasianstudies-ba-rendered-csv.html","collegeofliberalarts/sociology-ba-rendered-csv.html","collegeofliberalarts/spanish-ba-rendered-csv.html","collegeofliberalarts/sustainabilitystudies-ba-rendered-csv.html","collegeofliberalarts/urbanstudies-ba-rendered-csv.html","collegeofliberalarts/women'sandgenderstudies-ba-rendered-csv.html","collegeofliberalarts/planiihonorsprogram-ba-rendered-csv.html","collegeofliberalarts/behavioralandsocialdatascience-bsbsds-rendered-csv.html","collegeofliberalarts/economics-bseco-rendered-csv.html","collegeofliberalarts/geographicalsciences-bsenvirsci-rendered-csv.html","collegeofliberalarts/psychology-bspsy-rendered-csv.html","collegeofnaturalsciences/astronomy-ba-rendered-csv.html","collegeofnaturalsciences/chemistry-ba-rendered-csv.html","collegeofnaturalsciences/mathematics-ba-rendered-csv.html","collegeofnaturalsciences/physics-ba-rendered-csv.html","collegeofnaturalsciences/astronomy-bsa-rendered-csv.html","collegeofnaturalsciences/biology-bsa-rendered-csv.html","collegeofnaturalsciences/chemistry-bsa-rendered-csv.html","collegeofnaturalsciences/computerscience-bsa-rendered-csv.html","collegeofnaturalsciences/humandevelopmentandfamilysciences-bsa-rendered-csv.html","collegeofnaturalsciences/humanecology-bsa-rendered-csv.html","collegeofnaturalsciences/mathematics-bsa-rendered-csv.html","collegeofnaturalsciences/neuroscience-bsa-rendered-csv.html","collegeofnaturalsciences/nutrition-bsa-rendered-csv.html","collegeofnaturalsciences/physics-bsa-rendered-csv.html","collegeofnaturalsciences/astronomy-bsast-rendered-csv.html","collegeofnaturalsciences/biochemistry-bsbioch-rendered-csv.html","collegeofnaturalsciences/biology-bsbio,microbiologyandinfectiousdiseases-rendered-csv.html","collegeofnaturalsciences/chemistry-bsch-rendered-csv.html","collegeofnaturalsciences/computerscience-bscompsci-rendered-csv.html","collegeofnaturalsciences/biologicalsciences-bsenvirsci-rendered-csv.html","collegeofnaturalsciences/humandevelopmentandfamilysciences-bshdfs-rendered-csv.html","collegeofnaturalsciences/mathematics-bsmath-rendered-csv.html","collegeofnaturalsciences/medicallaboratoryscience-bsmedlabsci-rendered-csv.html","collegeofnaturalsciences/neuroscience-bsneurosci-rendered-csv.html","collegeofnaturalsciences/nutrition-bsntr-rendered-csv.html","collegeofnaturalsciences/physics-bsphy-rendered-csv.html","collegeofnaturalsciences/publichealth-bspublichealth-rendered-csv.html","collegeofnaturalsciences/statisticsanddatascience-bssds-rendered-csv.html","collegeofnaturalsciences/textilesandapparel-bsta-rendered-csv.html","schoolofnursing/nursing-bsn-rendered-csv.html","lyndonb.johnsonschoolofpublicaffairs/publicaffairs-bapubaff-rendered-csv.html","stevehicksschoolofsocialwork/socialwork-bsw-rendered-csv.html"]
print(len(degreelist))
# %%
