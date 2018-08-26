from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import time

# Initialize browser
def init_browser():
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    
    # # NASA Mars News
    # Initialize browser
    browser = init_browser()
    
    # Create a dictionary for storing all scraped data
    mars_data = {}

    # URL of NASA Mars News Site to be scraped
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # 5 second wait for loading data
    time.sleep(5)

    # HTML object
    html = browser.html
    
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')
    
    # Retrieve the latest news title and paragraph text and assign correponding variables
    news = soup.find('div', class_='list_text')
    title = news.find('div', class_='content_title').text
    text = news.find('div', class_='article_teaser_body').text

    # Add the news title and paragraph text to dictionary
    mars_data['title'] = title
    mars_data['text'] = text

    # # JPL Mars Space Images - Featured Image
    # Initialize browser
    browser = init_browser()

    # URL of JPL Featured Space Image to be scraped using Splinter
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)

    # Click on "Full Image" button
    browser.find_by_id('full_image').click()

    # HTML object
    html = browser.html
    
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Get relative path of full image
    image_url = soup.find("a", class_="button fancybox")['data-fancybox-href']
   
    # Create variable for base URL 
    base_url = 'https://www.jpl.nasa.gov'

    # Create full URL for featured image
    featured_image_url = base_url + image_url

    # Add featured image URL to dictionary
    mars_data['featured_image_url'] = featured_image_url

    # # Mars Facts
    # Initialize browser
    browser = init_browser()
    
    # Visit the Mars Facts Webpage
    url = 'http://space-facts.com/mars/'
    browser.visit(url)

    # Use Pandas to scrape the table containing Mars facts
    table = pd.read_html(url)

    # Select table
    mars_facts_DF = table[0]

    # Format table by adding column names and setting index
    mars_facts_DF.columns = ['Description', 'Values']
    mars_facts_DF = mars_facts_DF.set_index('Description')

    # Use Pandas to convert the data to a HTML table string and store in variable
    mars_table = mars_facts_DF.to_html().replace('\n', ' ')

    # Add mars facts to dictionary
    mars_data['mars_table'] = mars_table

    # # Mars Hemispheres
    # Initialize browser
    browser = init_browser()
    
    # Visit the USGS Astrogeology site 
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)

    # HTML object
    html = browser.html
    
    # Parse HTML with Beautiful Soup
    soup = bs(html, 'html.parser')

    # Lists to store hemisphere title and full image URL
    hemisphere_image_urls = []

    # Loop through all products and get relevant information
    for x in range(4):
    
        # Identify item link and click on it
        item = browser.find_by_tag('h3')
        item[x].click()
    
        # Create HTML browser object and parse with Beautiful Soup
        html = browser.html
        soup = bs(html, 'html.parser')
    
        # Get hemisphere title and full image URL
        img_title = soup.find('h2', class_='title').text
        img_url = soup.find('a', target='_blank')['href']
    
        # Create dictionary and append to list storing all hemisphere titles and image URLs.
        dictionary = {"title":img_title,"img_url":img_url}
        hemisphere_image_urls.append(dictionary)
       
        # Click on Back button to return to previous site
        browser.back()

    # Add list storing all hemisphere titles and image URLs to mars data dict
    mars_data['hemisphere_image_urls'] = hemisphere_image_urls

    # Print mars_info dictionary
    return mars_data