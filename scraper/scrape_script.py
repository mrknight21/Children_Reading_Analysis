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

request = "../info/books.txt"
with open(request) as f:
    text = f.read()
    books = [s for s in text.splitlines()]


columns = ['title', 'author', 'genre','page number','rating', 'educational', 'message', 'role_model', 'violence', 'sex', 'language', 'consumerism', 'drugs']
attributes = columns[5:]

df = pd.DataFrame(columns=columns)


for i in range(len(books)):
    item = books[i]

##read and load books
##example of item title: Pride and Prejudice by Jane Austen (6300)
##will need to do language detection?


    title = None
    author = None
    query = None
    bre = item.index("(")-1

    if ("by" in item):
        by = item.index("by")
        title = item[:by].strip()
        author = item[by+3:bre]
    else:
        title = item[:bre].strip()
        
    if(";" in title):
        title = title[:title.index(";")]

##require name pre processing to query
    query = title.lower().replace(" ", "-")

    
    
    
    url = "https://www.commonsensemedia.org/book-reviews/{}".format(query)
    url_get = requests.get(url)
    soup = bs4.BeautifulSoup(url_get.content, 'html.parser')
    
    if (soup.title.text == 'Page Not Found | Common Sense Media'):
        print("page not found")
        continue
    
    
    info = soup.find("ul", id='review-product-details-list')
    
    
#    web_auth = info.find(property='author').text
#    if(web_auth.lower() != author.lower()):
#        continue
    review_class = soup.find('div', 'csm_review')['class'][2]
    overall = re.sub('[^0-9]','', review_class)
    genre = info.find('strong',string="Genre:").next_sibling.next_sibling.text
    pgn = info.find('strong',string="Number of pages:").next_sibling
    pgn = int(pgn.strip())
    
    
    bookinfo = []
    bookinfo.append(title)
    bookinfo.append(author)
    bookinfo.append(genre)
    bookinfo.append(pgn)
    bookinfo.append(overall)
    
    
    for i in range(len(attributes)):
        target = attributes[i]
        container = soup.find("div", id="content-grid-item-{}".format(target))
        if(container != None):
            rating_class = container.find("div", "content-grid-rating")['class'][1]
            rating = re.sub('[^0-9]','', rating_class)
            print(target+" :"+rating)
            bookinfo.append(rating)
        else: 
            print(target + "NaN")
            bookinfo.append(None)
            
    print(bookinfo)
    bookdf = pd.DataFrame.from_records([tuple(bookinfo)], columns= columns)      
    df= df.append(bookdf)
    
df.to_csv("children_rating.csv", encoding='utf-8', index=False)


    
    