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