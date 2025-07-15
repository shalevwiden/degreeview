# Course Scraping

## For the creation of DegreeView

---

This is indeed rather complicated.
Alot of functions to break down.

I could make a substack post explaining this with a very nicely formatted markdown document.

first commit:

```bash
git commit -m"initialized repo for college_course_scraping, added README, .gitignore, and all python files"
```

scrapesemesterdata.py includes coursetype:

- Core,
- General Education
- Major
- Elective
- Opportunity

It scrapes all courses and seperates them by semester, primed for visualization with Excel, Matplotlib, or Mermaid.

I highly value making code slighly more complicated and adding a ton of comments everywhere for better understanding when going back to the code and better readability. In this project I have certainly needed it.

I utilized helper projects as well. Such as one to help me clear folders when I needed to create new files.

Came up with an innovative solution to print items in a csv horizontally.

Create both horizontal AND vertical fuk it.

### Excel Files creation with OpenPyXL

- Created responsive data creation, including a responsive border that goes around all data.

### Mermaid Creation and Mermaid CLI

- Used mmd.js and the mermaid CLI to create mermaid files and then used subprocess to save them to specified file locations.
  <br>
  This project is simply complicated. Heres a mermaid to explain the mermaid part.

  ```mermaid
  graph TD
  subgraph process
  makemmd("make mmd files for diagram")
  makepng("make png from mmd using mmd CLI")
  makepdf("Use pillow to make pdfs from the pngs")
  makeoverlay("Use reportlab canvas to make logo and heading pdf overlay")
  mergeo("Merge overlay and pdf")
  combinewlegend("Combine merged overlay and pdf with static legend pdf)
  end
  subgraph makelegend
  makelegendmmd("Make legend mmd code")
  makepng("Make legend png and then pdf")
  makelegendoverlay("Make legend overlay")
  mergesl("Merge secondary overlay with pdf")
  end
  ```
