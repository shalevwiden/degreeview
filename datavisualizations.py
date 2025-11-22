import os
from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
plt.rcParams['font.family'] = 'Helvetica'



from theassetcontainment import theasset

schoolcolordict={'School of Architecture':'#cdbee9', 'Red McCombs School of Business':'#f9e4af', 
 'School of Civic Leadership':"#7b6a57", 'Moody College of Communication':'#7e0107',
   'College of Education':'#86dff5', 'Cockrell School of Engineering':'#e35501', 
   'College of Fine Arts':"#633224", 'John A. and Katherine G. Jackson School of Geosciences':'#a3d29c', 
   'School of Information':'#2bc5e0', 
 'College of Liberal Arts':'#f3f3f3', 'College of Natural Sciences':'#f6c44b', 'School of Nursing':'#e3971f',
  'College of Pharmacy':"#BAB86C", 'Lyndon B. Johnson School of Public Affairs':'#096c6c', 'Steve Hicks School of Social Work':'#f0b420'}

biglist=[['School of Architecture', 5], ['Red McCombs School of Business', 9], ['School of Civic Leadership', 1], ['Moody College of Communication', 7], ['College of Education', 8], ['Cockrell School of Engineering', 11], ['College of Fine Arts', 16], ['John A. and Katherine G. Jackson School of Geosciences', 8], ['School of Information', 2], ['College of Liberal Arts', 42], ['College of Natural Sciences', 29], ['School of Nursing', 1], ['Lyndon B. Johnson School of Public Affairs', 1], ['Steve Hicks School of Social Work', 1]]
print(f'testing{list(schoolcolordict)[1]}')
biglist=sorted(biglist, key=lambda x: x[1])

# add colors to each sublist
for school in range(len(schoolcolordict)):
    for i in range(len(biglist)):
        if list(schoolcolordict)[school] in biglist[i][0]:
            biglist[i].append(schoolcolordict[list(schoolcolordict)[school]])
# that worked

labels = []
data = []
# or change this for more colors
colors=[]

for i in biglist:
    labels.append(i[0])
    data.append(i[1])
    # change this
    colors.append(i[2])

def make_autopct(values):
    def my_autopct(pct):
        total = sum(values)
        val = int(round(pct * total / 100.0))
        return f'{val}'
    return my_autopct

fig, ax = plt.subplots(figsize=(14, 8))  # Single figure

# Pie chart
wedges, texts, autotexts = ax.pie(
    data,
    labels=labels,
    colors=colors,
    startangle=110,
    autopct=make_autopct(data),
    textprops={'fontsize': 9}
)

# Hide specific labels and build legend
target_labels = [
    'Steve Hicks School of Social Work',
    'Lyndon B. Johnson School of Public Affairs',
    'School of Nursing',
    "School of Civic Leadership"
]

legend_patches = []

for label_text, text, wedge in zip(labels, texts, wedges):
    if label_text in target_labels:
        text.set_text('')  # Hide label on pie
        patch = mpatches.Patch(color=wedge.get_facecolor(), label=label_text)
        legend_patches.append(patch)

# Add legend outside the plot
legend=ax.legend(
    handles=legend_patches,
    loc='lower right',
    bbox_to_anchor=(1.1, -.1),  # (x, y) relative to the axes
    frameon=False,
    fontsize=8
)
legend.get_frame().set_edgecolor('black')
legend.get_frame().set_linewidth(1)
legend.get_frame().set_facecolor('white')  


# Title & Equal Aspect Ratio
ax.set_title("Number of Degree Programs at Schools at UT Austin ", pad=40,fontdict={'fontsize': 20, 'fontname': 'Helvetica', 'fontweight': 'bold'})
ax.axis('equal')


# plt.savefig("/Users/shalevwiden/Downloads/Projects/degreeviewwebsite/metaassets/degreeprogramcount",dpi=300)
# plt.show()
