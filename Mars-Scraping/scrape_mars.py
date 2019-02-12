# import dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import time

def scrape():
    # Store dictionary of scraped results
    results={}

    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    url='https://mars.nasa.gov/news/'

    # Requests pulls up different html than browser after scripts run
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)

    browser.visit(url)

    time.sleep(5)
    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')

    result = soup.find('div',class_='list_text')


    # Assign the text to variables that you can reference later.
    news_title = result.find('a').text
    news_p = result.find('div',class_='article_teaser_body').text

    results['news_title'] = news_title
    results['news_p'] = news_p

    # Visit the url for JPL Featured Space Image here.
    url='https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    # Use splinter to navigate the site and find the image url for the current Featured Mars Image
    browser.visit(url)

    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(2) #allow time for button to appear
    browser.click_link_by_partial_text('more info')

    html=browser.html
    soup = BeautifulSoup(html, 'html.parser')

    result=soup.find('figure', class_='lede')
    imgsource=result.find('a')['href']


    # assign the url string to a variable called featured_image_url.
    featured_image_url='https://www.jpl.nasa.gov'+imgsource

    results['featured_image_url'] = featured_image_url

    #  Visit the Mars Weather twitter account
    # scrape the latest Mars weather tweet from the page.
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    url='https://twitter.com/marswxreport?lang=en'

    # Retrieve page with the requests module
    response = requests.get(url)
    # Create BeautifulSoup object; parse with 'html'
    soup = BeautifulSoup(response.text, 'html')

    result = soup.find('p',class_='tweet-text')

    # Save the tweet text for the weather report as a variable called mars_weather.
    mars_weather = result.text

    results['mars_weather'] = mars_weather

    # Visit the Mars Facts webpage
    # use Pandas to scrape the table containing facts about the planet
    # including Diameter, Mass, etc.
    url = 'https://space-facts.com/mars/'

    table = pd.read_html(url)
    mars_df = table[0]
    mars_df.columns = ['','Data']
    mars_df.set_index('',inplace=True)


    # Use Pandas to convert the data to a HTML table string.
    mars_table = mars_df.to_html()
    mars_table.replace('\n','')
    with open('mars_table.html', 'w') as fo:
        fo.write(mars_table)

    results['mars_table'] = mars_table

    # Visit the USGS Astrogeology site to obtain
    # high resolution images for each of Mar's hemispheres.
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    img_base = 'https://astrogeology.usgs.gov'

    hemispheres = ["Valles Marineris Hemisphere",
                   "Cerberus Hemisphere",
                   "Schiaparelli Hemisphere",
                   "Syrtis Major Hemisphere"]
    hemisphere_image_urls = []

    for hemisphere in hemispheres:
    #     You will need to click each of the links to the hemispheres
    #     in order to find the image url to the full resolution image.
        browser.visit(url)
        browser.click_link_by_partial_text(hemisphere)

        html = browser.html
        soup = BeautifulSoup(html, 'html.parser')

        result = soup.find('img',class_='wide-image')['src']
        img_url = img_base + result
    #     Append the dictionary with the image url string and the hemisphere title to a list.
    #     This list will contain one dictionary for each hemisphere.
        entry={'title': hemisphere, 'img_url': img_url}
        hemisphere_image_urls.append(entry)

    browser.quit()

    results['hemisphere_image_urls'] = hemisphere_image_urls

    return results
