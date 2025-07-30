import os
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.font_manager import FontProperties

import numpy as np

plt.style.use('fivethirtyeight') # Example: applying the 'ggplot' style
print(plt.style.available)
plt.rcParams['font.family'] = 'Helvetica'



barlow_path = "/Users/shalevwiden/Downloads/Barlow,Roboto/Barlow/Barlow-SemiBold.ttf"
roboto_bold = FontProperties(fname="/Users/shalevwiden/Downloads/Barlow,Roboto/Roboto/static/RobotoBlack.ttf")



from theassetcontainment import theasset
biglist=[[['Interior Design (BSID)', 'Architecture (BArch)', 'Architecture-Architectural Engineering (BArch-BSArchE)', 'Architecture-Plan II Honors (BArch-BA)', 'Architectural Studies (BSAS)'], [125, 161, 195, 186, 125], [83, 88, 135, 130, 61]], [['Accounting (BBA)', 'Business Analytics (BBA)', 'Business Administration, Honors track (BBA)', 'Finance (BBA)', 'International Business (BBA)', 'Management  (BBA)', 'Management Information Systems (BBA)', 'Marketing  (BBA)', 'Supply Chain Management (BBA)'], [120, 120, 120, 120, 120, 120, 120, 120, 120], [59, 60, 63, 59, 71, 53, 60, 51, 56]], [['Civics Honors (BA)'], [120], [0]], [['Advertising (BSAdv)', 'Communication and Leadership (BSComm&Lead)', 'Communication Studies (BSCommStds)', 'Journalism (BJ)', 'Public Relations (BSPR)', 'Radio-Television-Film (BSRTF)', 'Speech,Language, and Hearing Sciences (BSSLH)'], [120, 120, 120, 120, 120, 120, 120], [42, 36, 36, 39, 42, 36, 42]], [['Athletic Training (BSAthTrng)', 'Education (BSEd)', 'Youth and Community Studies (BSEd)', 'Applied Movement Science (BSKin&Health)', 'Exercise Science (BSKin&Health)', 'Health Promotion and Behavioral Science (BSKin&Health)', 'Physical Culture and Sports Studies (BSKin&Health)', 'Sport Management (BSKin&Health)'], [120, 111, 120, 120, 120, 120, 120, 120], [50, 60, 60, 73, 88, 60, 54, 57]], [['Aerospace Engineering (BSAsE)', 'Architectural Engineering (BSArchE)', 'Biomedical Engineering (BSBiomedE)', 'Chemical Engineering (BSChE)', 'Civil Engineering (BSCE)', 'Computational Engineering (BSCompE)', 'Electrical and Computer Engineering (BSECE)', 'Environmental Engineering (BSEnvE)', 'Geosystems Engineering (BSGE)', 'Mechanical Engineering (BSME)', 'Petroleum Engineering (BSPE)'], [127, 126, 132, 129, 124, 122, 125, 125, 132, 126, 128], [63, 84, 70, 60, 84, 68, 65, 81, 90, 73, 89]], [['Acting (BFA)', 'Art Education (BFA)', 'Dance (BFA)', 'Design (BFA)', 'Studio Art (BFA)', 'Theatre Education (BFA)', 'Composition (BMusic)', 'Jazz (BMusic)', 'Music Performance (BMusic)', 'Music Studies (BMusic)', 'Art History (BA)', 'Design (BA)', 'Studio Art (BA)', 'Theatre and Dance (BATD)', 'Music (BAMusic)', 'Arts and Entertainment Technologies (BSAET)'], [117, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120], [66, 72, 71, 67, 72, 78, 75, 68, 94, 87, 39, 43, 42, 54, 67, 57]], [['Geosciences (BAGS)', 'Geosciences (BSEnvirSci)', 'Climate System Science (BSGS)', 'General Geology (BSGS)', 'Geophysics (BSGS)', 'Geosciences (BSGS)', 'Hydrology and Water Resources (BSGS)', 'Geosystems Engineering (BSGE)'], [120, 126, 123, 126, 126, 126, 126, 132], [45, 78, 58, 61, 41, 41, 57, 90]], [['Informatics (BA)', 'Informatics (BSI)'], [120, 120], [39, 30]], [['African and African Diaspora Studies (BA)', 'American Studies (BA)', 'Anthropology (BA)', 'Asian Cultures and Languages (BA)', 'Asian Studies (BA)', 'Classical Languages (BA)', 'Classical Studies (BA)', 'Economics (BA)', 'English (BA)', 'Ethnic Studies (BA)', 'European Studies (BA)', 'French Studies (BA)', 'Geography (BA)', 'German (BA)', 'Government (BA)', 'Health and Society (BA)', 'History (BA)', 'Human Dimensions of Organizations (BA)', 'Humanities (BA)', 'International Relations and Global Studies (BA)', 'Italian Studies (BA)', 'Jewish Studies (BA)', 'Latin American Studies (BA)', 'Linguistics (BA)', 'Mexican American and Latina-o Studies (BA)', 'Middle Eastern Studies (BA)', 'Philosophy (BA)', 'Psychology (BA)', 'Race,Indigeneity, and Migration (BA)', 'Religious Studies (BA)', 'Rhetoric and Writing (BA)', 'Russian,East European, and Eurasian Studies (BA)', 'Sociology (BA)', 'Spanish (BA)', 'Sustainability Studies (BA)', 'Urban Studies (BA)', "Women's and Gender Studies (BA)", 'Plan II Honors Program (BA)', 'Behavioral and Social Data Science (BSBSDS)', 'Economics (BSECO)', 'Geographical Sciences (BSEnvirSci)', 'Psychology (BSPsy)'], [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 117, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 117, 120, 120, 120, 126, 120], [36, 48, 48, 39, 42, 64, 70, 56, 51, 39, 48, 42, 46, 36, 42, 42, 36, 45, 39, 48, 39, 42, 42, 36, 51, 63, 48, 40, 42, 48, 42, 42, 45, 45, 39, 48, 45, 27, 22, 41, 71, 49]], [['Astronomy (BA)', 'Chemistry (BA)', 'Mathematics (BA)', 'Physics (BA)', 'Astronomy (BSA)', 'Biology (BSA)', 'Chemistry (BSA)', 'Computer Science (BSA)', 'Human Development and Family Sciences (BSA)', 'Human Ecology (BSA)', 'Mathematics (BSA)', 'Neuroscience (BSA)', 'Nutrition (BSA)', 'Physics (BSA)', 'Astronomy (BSAst)', 'Biochemistry (BSBioch)', 'Biology (BSBio), Microbiology and Infectious Diseases', 'Chemistry (BSCh)', 'Computer Science (BSCompSci)', 'Biological Sciences (BSEnvirSci)', 'Human Development and Family Sciences (BSHDFS)', 'Mathematics (BSMath)', 'Medical Laboratory Science (BSMedLabSci)', 'Neuroscience (BSNeurosci)', 'Nutrition (BSNtr)', 'Physics (BSPhy)', 'Public Health (BSPublichealth)', 'Statistics and Data Science (BSSDS)', 'Textiles and Apparel (BSTA)'], [120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 120, 124, 120, 120, 123, 120, 120, 120, 120, 126, 120, 120, 120, 120, 120, 126, 120, 120, 120], [43, 47, 32, 52, 60, 68, 56, 70, 70, 61, 50, 77, 76, 58, 79, 78, 84, 78, 58, 77, 73, 58, 63, 67, 95, 70, 66, 57, 69]], [['Nursing (BSN)'], [122], [61]], [['Public Affairs (BAPubAff)'], [123], [36]], [['Social Work (BSW)'], [122], [34]]]
combinedlist=[]
print('\n\ntesting\n\n')
for school in biglist:
    for i in range(len(school[0])):

        names=school[0]
        totalhours=school[1]
        majhours=school[2]
        degreelist=[names[i],totalhours[i],majhours[i]]
        combinedlist.append(degreelist)
        if "economics" in degreelist[0].lower():
            print(degreelist)
        
# print(combinedlist)

totalsorted=sorted(combinedlist,key=lambda x:x[1],reverse=True)[0:16]
majorsorted=sorted(combinedlist,key=lambda x:x[2],reverse=True)[0:11]
majorsortedlow=sorted(combinedlist,key=lambda x:x[2],reverse=False)[:16]
print(f'Majors sorted low:\n\n')
print(majorsortedlow)
print(f'\n\n\nMajors sorted high:\n\n')
print(majorsorted)


def plottotal(sortedlist):
    labels=[]
    values=[]
    for i in sortedlist:
        labels.append(i[0])
        values.append(i[1])
    print('printing labels and values\n\n\n')
    print(labels,values)
    # labels=sorted(labels,reverse=True)
    # values=sorted(values,reverse=True)



    # Plot
    sorted_pairs = sorted(zip(values, labels), reverse=True)
    values_sorted, labels_sorted = zip(*sorted_pairs[::-1])

# Create the horizontal bar chart
    cmap = plt.get_cmap('tab20')

    colors = cmap(np.arange(len(labels)))
    plt.figure(figsize=(9, 8))

    bars = plt.barh(labels_sorted, values_sorted,color=colors)
    plt.gca().set_yticklabels([])

    # Add value labels inside each bar
    for bar, label,value in zip(bars, labels_sorted,values_sorted):
        plt.text(5,                    # small indent inside bar from the left
                bar.get_y() + bar.get_height() / 2,
                f"{label}: {value}",
                va='center',
                ha='left',
                fontproperties=roboto_bold,
         color='white',
         fontsize=9)

    # Titles and labels

    plt.title("Top 15 Degrees by Hours", fontproperties='barlow_path', fontsize=16,fontweight='bold')
    plt.xticks(range(0, 201, 10))  # Set ticks at intervals of 10

    plt.xlabel("Hours", fontname='Helvetica', fontsize=13,labelpad=12)
    plt.ylabel("Degree",  fontname='Helvetica', fontsize=13,labelpad=12)

    # Show chart
    plt.savefig("/Users/shalevwiden/Downloads/Projects/degreeviewwebsite/metaassets/topdegreehours.png",dpi=300)

    plt.show()


def plotmajor(sortedlist):
    labels=[]
    values=[]
    for i in sortedlist:
        labels.append(i[0].replace('-','/'))
        values.append(i[2])
    print('printing labels and values\n\n\n')
    print(labels,values)
    # labels=sorted(labels,reverse=True)
    # values=sorted(values,reverse=True)



    # Plot
    sorted_pairs = sorted(zip(values, labels), reverse=True)
    values_sorted, labels_sorted = zip(*sorted_pairs[::-1])

# Create the horizontal bar chart
    cmap = plt.get_cmap('tab20c')
    colors = cmap(np.arange(len(labels)))
    plt.figure(figsize=(9, 8))

    bars = plt.barh(labels_sorted, values_sorted,color=colors)
    plt.gca().set_yticklabels([])

    # Add value labels inside each bar
    for bar, label,value in zip(bars, labels_sorted,values_sorted):
        plt.text(5,                    # small indent inside bar from the left
                bar.get_y() + bar.get_height() / 2,
                f"{label}: {value}",
                va='center',
                ha='left',
                fontproperties=roboto_bold,
         color='white',
         fontsize=9)

    # Titles and labels

    plt.title("Top 10 Degrees by Major Classified Hours", fontproperties='barlow_path', fontsize=16,fontweight='bold')
    plt.xticks(range(0, 141, 10))  # Set ticks at intervals of 10

    plt.xlabel("Major Hours", fontname='Helvetica', fontsize=13,labelpad=12)
    plt.ylabel("Degree",  fontname='Helvetica', fontsize=13,labelpad=12)
   

    # Show chart
    
    plt.savefig("/Users/shalevwiden/Downloads/Projects/degreeviewwebsite/metaassets/topmajorhours.png",dpi=300)

    plt.show()
    


def plotmajorlow(sortedlist):
    labels=[]
    values=[]
    for i in sortedlist:
        labels.append(i[0].replace('-','/'))
        values.append(i[2])
    
    # labels=sorted(labels,reverse=True)
    # values=sorted(values,reverse=True)



    # Plot
    sorted_pairs = sorted(zip(values, labels), reverse=True)
    values_sorted, labels_sorted = zip(*sorted_pairs)

# Create the horizontal bar chart
    cmap = plt.get_cmap('tab20c')

    colors = cmap(np.arange(len(labels)))
    plt.figure(figsize=(9, 8))

    bars = plt.barh(labels_sorted, values_sorted,color=colors)
    plt.gca().set_yticklabels([])

    # Add value labels inside each bar
    for bar, label,value in zip(bars, labels_sorted,values_sorted):
        plt.text(5,                    # small indent inside bar from the left
                bar.get_y() + bar.get_height() / 2,
                f"{label}: {value}",
                va='center',
                ha='left',
                color='white',
                fontsize=9)

    # Titles and labels

    plt.title("Top degrees by Least Number of Major Classified Hours", fontproperties='barlow_path', fontsize=16,fontweight='bold')
    plt.xticks(range(0, 50, 5))  # Set ticks at intervals of 10

    plt.xlabel("Major Hours", fontname='Helvetica', fontsize=13,labelpad=12)
    plt.ylabel("Degree",  fontname='Helvetica', fontsize=13,labelpad=12)
   

    # Show chart
    
    plt.savefig("/Users/shalevwiden/Downloads/Projects/degreeviewwebsite/metaassets/lowmajorhours.png",dpi=300)

    plt.show()
plottotal(sortedlist=totalsorted)

plotmajor(sortedlist=majorsorted)


