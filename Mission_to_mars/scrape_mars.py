import requests
import os
import pymongo
import pandas as pd 
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager

def scrape():
    # *****************************************Part 1*****************************************
    conn = 'mongodb://localhost:27017'
    client = pymongo.MongoClient(conn)

    filepath = os.path.join("mars1.html")
    with open(filepath, encoding='utf-8') as file:
        html = file.read()

    soup = BeautifulSoup(html, 'html.parser')
    results_titles = soup.find_all('div', class_='content_title')
    results_paragraphs = soup.find_all('div', class_='article_teaser_body')
    title = str(results_titles[0].text)
    paragraph = str(results_paragraphs[0].text)
   
    # *****************************************Part 2*****************************************
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    html = browser.html
    soup0 = BeautifulSoup(html, 'html.parser')
    results0 = soup0.find_all('img')
    featured_image_url = url + '/' +results0[1]['src']
    # https://spaceimages-mars.com/image/featured/mars2.jpg

    # *****************************************Part 3*****************************************
    url = "https://galaxyfacts-mars.com"
    tables = pd.read_html(url)
    mars_earth_table = pd.DataFrame(tables[0][1:])
    rm = mars_earth_table.rename(columns = {1:'Mars',2:'Earth'}, index = mars_earth_table[0])
    final_table = rm.drop(columns = [0])

    # *****************************************Part 4*****************************************
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    base_url = "https://marshemispheres.com"
    # browser.visit(url)
    image_urls = [
        'https://marshemispheres.com/cerberus.html',
        'https://marshemispheres.com/schiaparelli.html',
        'https://marshemispheres.com/syrtis.html',
        'https://marshemispheres.com/valles.html']

    # create the list of dictionaries containing image information
    hemisphere_image_urls = []
    for url in image_urls:
        browser.visit(url)
        html = browser.html
        sp = BeautifulSoup(html, 'html.parser')
        #get the enhanced image url
        description = sp.findAll('div', class_ = 'description')
        enhanced_url = description[0].find_all('dd')[1].find('a')['href']
        
        #get the titles 
        title = sp.findAll('h2',class_ = "title")
        enh_title = title[0].text.split()[:-1]
        t = " ".join(enh_title)

        #create dictionary element for dictionary list
        dt = {'Title':t,"Image Url":base_url+'/'+enhanced_url}
        hemisphere_image_urls.append(dt)

    # return everything that was collected as a dictionary 
    return {'Latest News':[title,paragraph], 'Featured Image':featured_image_url,
            'Comparison Table':final_table, 'Enhanced Pictures':hemisphere_image_urls}

print(scrape())