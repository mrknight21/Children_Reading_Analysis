# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import numpy as np
import bs4
import nltk
import urllib
import requests

request = "books.txt"


columns = ['title', 'author', '']


with open(request) as f:
    #read and load books
    text = f.read()
    books = [s for s in text.splitlines()]
    

url = "https://www.commonsensemedia.org/book-reviews/pride-and-prejudice"



url_get = requests.get(url)
soup = bs4.BeautifulSoup(url_get.content, 'html.parser')


ed_value = soup.find("div", id="content-grid-item-educational")




result = re.sub('[^0-9]','', a)

pos_msg = None
pos_RM = None
violence = None
sex = None
language = None
consumerism = None
Drinking_drug_smoke = None


print(soup.contents)