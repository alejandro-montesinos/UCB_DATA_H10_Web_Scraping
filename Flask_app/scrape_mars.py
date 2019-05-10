#******************************************************************************
# UC Berkeley Extension Data Analytics Program
# Homework 10: Web Scraping and Mongo
# Task: Mission to Mars
# Submitted by: Alejandro Montesinos
# Date: May 9, 2019
#******************************************************************************

#Settings
from   bs4      import BeautifulSoup
from   splinter import Browser
import pandas   as     pd
import datetime as     dt

#Visit the NASA mars NEWS SITES
def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    # Visit the mars nasa new site
    browser.visit(url)

    # Get first list item and wait half a second if not immediately present
    browser.is_element_present_by_css('ul.item_list li.slide', wait_time=0.5)
    html = browser.html
    news_soup = BeautifulSoup(html, 'html.parser')
    try:
        slide_element = news_soup.select_one('ul.item_list li.slide')
        slide_element.find("div", class_="content_title")
        # Use the parent element to find the first a tag and save it as news_title
        news_title = slide_element.find('div', class_="content_title").get_text()
        news_paragraph = slide_element.find('div', class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None
    return news_title, news_paragraph


def featured_image(browser):
    url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url)
    #Asking splinter to go to the site hit a button with class name full_image
    # <button class = "full_image">Full Image</button>
    full_image_button = browser.find_by_id('full_image')
    full_image_button.click()
    #Fin the more info button and click on that 
    browser.is_element_present_by_text('more info', wait_time=1)
    more_info_element = browser.find_link_by_partial_text('more info')
    more_info_element.click()
    #Parse the results html with beautiful soup 
    html = browser.html
    image_soup = BeautifulSoup(html, 'html.parser')

    img = image_soup.select_one('figure.lede a img')
    try:
        img_url = img.get('src')
    except AttributeError:
       return None
    img_url = f'https://www.jpl.nasa.gov{img_url}'
    return img_url

def twitter_weather(browser):
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')
    #First find a tweet with the data-name 'Mars Weather'
    mars_weather_tweet = weather_soup.find('div', attrs = {"class": "tweet", "data-name": "Mars Weather"})
    #Next searh within the tweet for p tag containing the tweet text
    mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()
    return mars_weather

def hemisphere(browser):
   url = 'https://astrogeology.usgs.gov/search/results?q=hemispher+enhanced&k1=target&v1=Mars'
   browser.visit(url)
   hemisphere_image_urls = []
   links = browser.find_by_css('a.product-item h3')
   return print(links)


def hemisphere(browser):
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image_urls = []

    # First get a list og all the hemisphers
    links = browser.find_by_css('a.product-item h3')
    for item in range(len(links)):
        hemisphere = {}        
        # We have to find the element on each loop to avoid a stale element exception
        browser.find_by_css('a.product-item h3')[item].click()        
        # Next we find the Sample Image anchor tage and extract the href
        sample_element = browser.find_link_by_text('Sample').first
        hemisphere['img_url'] = sample_element['href']
        # Get Hemispher title 
        hemisphere['title'] = browser.find_by_css('h2.title').text
        #Append hemispher object to list
        hemisphere_image_urls.append(hemisphere)
        # Finally, we navigate backwards
        browser.back()
    return hemisphere_image_urls


def mars_facts():
    try: 
       df = pd.read_html('https://space-facts.com/mars/')[0]
    except BaseException:
        return None
    df.columns =['description', 'values']
    df.set_index('description', inplace=True) 
    return df.to_html()

#Set excecutable path and initialize the chrome browser
def scrape_all(): # main bot 
    executable_path = {'executable_path': '/usr/local/bin/chromedriver'}
    browser = Browser('chrome', **executable_path)
    news_title, news_paragraph = mars_news(browser)
    img_url = featured_image(browser)
    mars_weather = twitter_weather(browser)
    hemisphere_image_urls = hemisphere(browser)
    facts = mars_facts()
    timestamp = dt.datetime.now()

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": img_url,
        "hemispheres": hemisphere_image_urls,
        "weather": mars_weather,
        "facts": facts,
        "last_modified": timestamp
    }
    browser.quit()
    return data 


if __name__ == "__main__":
    print(scrape_all())

#******************************************************************************
# *** END OF CODE  ***
#******************************************************************************