#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from datetime import datetime
import requests
import os
import time


# In[3]:


#point to the directory where chromedriver exists
executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[4]:


#visit the NASA Mars site
url = "https://mars.nasa.gov/news/"
browser.visit(url)


# In[5]:


#Create a Beautiful Soup object - use bs to write it into HTML
html = browser.html
soup = bs(html,"html.parser")


# In[6]:


news_title = soup.find("div",class_="content_title").text
news_p = soup.find("div", class_="article_teaser_body").text
print(f"Title: {news_title}")
print(f"Para: {news_p}")


# JPL Mars Space Images - Featured Image

# In[7]:


url_image = "https://www.jpl.nasa.gov/spaceimages/?search=&category=featured#submit"
browser.visit(url_image)


# In[8]:


#Extract the base url
from urllib.parse import urlsplit
base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_image))
print(base_url)


# In[9]:


#Design an xpath selector to grab the image
xpath = "//*[@id=\"page\"]/section[3]/div/ul/li[1]/a/div/div[2]/img"


# In[10]:


#Use splinter to click on the mars featured image
#Obtain the full resolution image
results = browser.find_by_xpath(xpath)
img = results[0]
img.click()


# In[11]:


#Get image url using BeautifulSoup
html_image = browser.html
soup = bs(html_image, "html.parser")
img_url = soup.find("img", class_="fancybox-image")["src"]
full_img_url = base_url + img_url
print(full_img_url)


# Mars Weather

# In[12]:


url_facts = "https://space-facts.com/mars/"


# In[13]:


table = pd.read_html(url_facts)
table[0]


# In[14]:


df_mars_facts = table[0]
df_mars_facts.columns = ["Parameter", "Values"]
df_mars_facts.set_index(["Parameter"])


# In[15]:


mars_html_table = df_mars_facts.to_html()
mars_html_table = mars_html_table.replace("\n", "")
mars_html_table


# Mars Hemisperes

# In[16]:


url_hemisphere = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser.visit(url_hemisphere)


# In[17]:


#Extract the base url
hemisphere_base_url = "{0.scheme}://{0.netloc}/".format(urlsplit(url_hemisphere))
print(hemisphere_base_url)


# In[27]:


# scrape images of Mars' hemispheres from the USGS site
mars_hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
hemi_dicts = []

for i in range(1,9,2):
    hemi_dict = {}
    
    browser.visit(mars_hemisphere_url)
    time.sleep(1)
    hemispheres_html = browser.html
    hemispheres_soup = bs(hemispheres_html, 'html.parser')
    hemi_name_links = hemispheres_soup.find_all('a', class_='product-item')
    hemi_name = hemi_name_links[i].text.strip('Enhanced')
    
    detail_links = browser.find_by_css('a.product-item')
    detail_links[i].click()
    time.sleep(1)
    browser.find_link_by_text('Sample').first.click()
    time.sleep(1)
    browser.windows.current = browser.windows[-1]
    hemi_img_html = browser.html
    browser.windows.current = browser.windows[0]
    browser.windows[-1].close()
    
    hemi_img_soup = bs(hemi_img_html, 'html.parser')
    hemi_img_path = hemi_img_soup.find('img')['src']

    print(hemi_name)
    hemi_dict['title'] = hemi_name.strip()
    
    print(hemi_img_path)
    hemi_dict['img_url'] = hemi_img_path

    hemi_dicts.append(hemi_dict)


# In[ ]:





# In[ ]:




