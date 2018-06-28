# -*- coding: utf-8 -*-
"""
This is the scraper that scrape review informatino for books
"""

import pandas as pd
import numpy as np
import bs4
import nltk
import requests
import re

request = "./info/books.txt"
with open(request) as f:
    text = f.read()
    books = [s for s in text.splitlines()]


columns = ['title', 'author', 'genre','page number','rating', 'educational', 'message', 'role_model', 'violence', 'sex', 'language', 'consumerism', 'drugs']
attributes = columns[3:]

df = pd.DataFrame(columns=columns)


for i in range(len(books)):
    title = books[i]

 #read and load books

##will need to do language detection?



##require name pre processing to query
    query = "pride-and-prejudice"
    author = "Jane Austen"
    
    
    
    url = "https://www.commonsensemedia.org/book-reviews/{}".format(query)
    url_get = requests.get(url)
    soup = bs4.BeautifulSoup(url_get.content, 'html.parser')
    
    if (soup.title.text == 'Page Not Found | Common Sense Media'):
        continue
    
    
    info = soup.find("ul", id='review-product-details-list')
    web_auth = info.find(property='author').text
    
    
    if(web_auth.lower() != author.lower()):
        continue
    
    genre = info.find('strong',string="Genre:").next_sibling.next_sibling.text
    pgn = info.find('strong',string="Number of pages:").next_sibling
    
    
    bookinfo = []
    bookinfo.append(query)
    bookinfo.append(author)
    bookinfo.append(genre)
    
    
    for i in range(len(attributes)):
        target = attributes[i]
        container = soup.find("div", id="content-grid-item-{}".format(target))
        if(container != None):
            rating_class = container.find("div", "content-grid-rating")['class'][1]
            rating = re.sub('[^0-9]','', rating_class)
            print(target+" :"+rating)
            bookinfo.append(rating)
        else: 
            print(target + None)
            bookinfo.append(None)
            
    
    bookdf = pd.DataFrame.from_records([tuple(bookinfo)], columns= columns)      
    print(bookinfo)


