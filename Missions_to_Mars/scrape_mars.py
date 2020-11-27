
# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup as bs
import requests
import time
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape_info():
    # Configure settings for splinter
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=False)


    ### Part 1: NASA Mars News_________________________________________________________________________________________________________________________________
    # Visit mars.nasa.gov/news site
    # Get html and parse it from mars events website using requests
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Find most recent news article title and description
    a = soup.find("body", id="news")
    b = a.find("ul",class_="item_list")
    c = b.find("li",class_="slide")
    d = c.find("div",class_="image_and_description_container")
    e = d.find("div",class_="list_text")
    f = e.find("div",class_="content_title")

    news_title = f.find("a").text
    news_description = e.find("div",class_="article_teaser_body").text

    ###Part 2: JPL Mars Space Images Featured Image - Get html and parse it________________________________________________________________________________________________________________________________
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")
    # Find the featured image url
    # Click on FULL IMAGE button
    link1 = browser.find_by_tag('a').links.find_by_partial_text("FULL IMAGE")
    link2 = link1.click()
    time.sleep(10)
    # Click on More Info button
    link3 = browser.links.find_by_partial_text("more info")
    link3.click()
    time.sleep(10)
    #Save full size of featured image 
    link4 = browser.find_by_tag('figure[class="lede"]')
    link5 = link4.find_by_tag('a')
    for image in link5:
        featured_image_url = image["href"]

    ###Part 3: Mars Facts_______________________________________________________________________________________________________________________________________________________________________--
    #Scrape page into soup
    url = "https://space-facts.com/mars/"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")  

    a = soup.find("table",id="tablepress-p-mars-no-2")
    b = a.find_all("tr")
    metric = list()
    value = list()
    for row in b:
        metric.append(row.find("td",class_="column-1").text)
        value.append(row.find("td",class_="column-2").text)

    mars_facts = pd.DataFrame({'Metric': metric,
                            'Value' : value}, 
                            columns = ['Metric','Value'])
    mars_facts.set_index('Metric')
    # convert dataframe to html
    mars_facts_html = mars_facts.to_html()
    

    ###Part 4: Mars Hemispheres___________________________________________________________________________________________________________________________________________________________________________

    #Scrape page into soup
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    html = browser.html
    soup = bs(html, "html.parser")  

    # Find the body of the page that includes the necessary links for the hemispheres
    link1 = browser.find_by_tag('div[id="product-section"]')
    h_count = 0
    hemisphere_image_urls = list()

    # Within the div: product-section, there are 4 class items. Each one corresponds to a different hemisphere 
    while h_count < 4:
        
        # Initialize dictionary to store each hemisphere's information
        temp = dict()
        
        # Navigate to the hemisphere's section
        link2 = link1.find_by_tag('div[class="item"]')[h_count]
        link3 = link2.find_by_tag("a")
        link4 = link3.last
        link5 = link4.click()
        time.sleep(1)
        
        # Get the hemisphere name, store in a list
        hlink1 = browser.find_by_tag('section[class="block metadata"]')
        key = hlink1.find_by_tag('h2[class="title"]').text
        
        # Get the full size image url for each hemisphere
        hlink2 = browser.find_by_tag('div[id="wide-image"]')
        hlink3 = hlink2.find_by_tag('img[class="wide-image"]')
        value = hlink3['src']
        
        # Save the hemisphere's data in the temp dictionary, append the dictionary to the list
        temp[key]=value
        hemisphere_image_urls.append(temp)
        
        # Go back to the main page and start again for the next hemisphere
        link6 = browser.back()
        link1 = browser.find_by_tag('div[id="product-section"]')
        h_count +=1
  
    browser.quit()

    #Create a single dictionary of all the items
    # Create a single dictionary of the information

    mars_info = {"Recent_news_title": news_title,
                  "Recent_news_description": news_description,
                  "Featured_image_url": featured_image_url,
                  "Mars_facts_html": mars_facts_html,
                  "Hemispheres_images": hemisphere_image_urls} 


    return(mars_info)
