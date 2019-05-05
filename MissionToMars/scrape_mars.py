from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time



def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    mars = {}
    browser = init_browser()

     # NASA Mars News
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    mars["news_title"]  = soup.find('div', class_="content_title").a.text
    mars["news_p"] = soup.find('div', class_="article_teaser_body").text


    # #Mars Featured Image # #
    image_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    image = soup.find('a', class_='button fancybox')["data-fancybox-href"]
    mars["featured_image_url"] = 'https://www.jpl.nasa.gov' + image


    # # Mars Weather # #
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    time.sleep(10)

    mars["twit_url"] = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text


    # # Mars Facts # #
    url = 'https://space-facts.com/mars/'
    facts = pd.read_html(url)
    mars_facts_df = facts[0]
    mars_facts_df.columns = [" ", "value"]
    mars_facts_df.set_index(" ", inplace=True)


    html_table = mars_facts_df.to_html()
    mars["html_table"] = html_table.replace('\n', '')
  

    # # Mars Hemispheres # #
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, 'lxml')

    time.sleep(5)

    hemispheres = soup.find_all('div', class_='item')

    hemisphere_image_urls = []

    for hemisphere in hemispheres:
        time.sleep(2)
        title = hemisphere.find('h3').text
        item_url = hemisphere.find('a', class_='itemLink product-item')['href']
        url = 'https://astrogeology.usgs.gov' + item_url
        browser.visit(url)
        soup = BeautifulSoup(browser.html, 'html.parser')
        img_url = soup.find('div', class_='downloads').find("a")['href']
        hemisphere_image_urls.append({'title':title, 'img_url':img_url})
    
    mars["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()


    return(mars)











