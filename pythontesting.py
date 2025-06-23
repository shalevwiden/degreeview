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