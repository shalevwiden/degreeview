import requests
import bs4
from bs4 import BeautifulSoup

import sys
import os

import csv

# good to check everythings working with the venv:
if __name__=='__main__':
    print(f'the version of beautiful soup is\n {(bs4.__version__)}')
    print(f'the version of requests is\n {(requests.__version__)}')
    print(f'\nthe python version being used is:{sys.executable}\n')


# this script is gonna be.. huge
from theassetcontainment import theasset

from scrapesemesterdata import getallcourses_splitbysemester

class makeSemesterFiles:
    def __init__(self):
        pass
    def makecsvfiles(self):
        pass
    def make_excel_files(self):
        pass
    def make_mermaid_files(self):
        pass