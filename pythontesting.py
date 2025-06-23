print('\xa0')

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

