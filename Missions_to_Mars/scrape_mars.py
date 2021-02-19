# Dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
import pandas
from splinter import Browser
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "./chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    mars_data = {}

    url = "https://mars.nasa.gov/news/"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    print(soup.prettify())

    mars_data["title"] = soup.find("div", class_="content_title").get_text()
    mars_data["content"] = soup.find("div", class_="rollover_description").get_text()

    browser = init_browser()

    images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(images_url)

    # HTML object
    html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')
    # Retrieve all elements that contain book information
    images = soup.find_all('a', class_="button fancybox")

    # Iterate through each book
    for image in images:
        href = image["data-fancybox-href"]
        print('https://www.jpl.nasa.gov' + href)

        featured_image_url = 'https://www.jpl.nasa.gov' + href
    
        mars_data["featured"] = featured_image_url

    facts_url = "https://space-facts.com/mars/"
    table = pd.read_html(facts_url)
    facts_df = table[0]
    facts_df = facts_df.rename(columns={0:"Description", 1: "Value"})
    html_facts = facts_df.to_html()

    mars_data["facts"] = html_facts

    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    hemispheres_image_urls=[]

    links = browser.find_by_css("a.product-item h3")

    for l in range(len(links)):
        hemispheres={}
        browser.find_by_css("a.product-item h3")[l].click()
        sample_link = browser.links.find_by_text('Sample').first
        hemispheres['url'] = sample_link['href']
        hemispheres['title'] = browser.find_by_css('h2.title').text
        hemispheres_image_urls.append(hemispheres)
        browser.back()
    
    mars_data["hemispheres"] = hemispheres_image_urls
    
    browser.quit()

    return mars_data

