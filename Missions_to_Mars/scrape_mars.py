import pandas as pd
import time
from bs4 import BeautifulSoup as bs
from splinter import Browser
import os


def init_browser():
    executable_path={'executable_path':'/usr/local/bin/chromedriver'}
    browser=Browser('chrome',**executable_path,headless=False)
    return browser


def scrape():
    browser=init_browser()
    mars_data={}
    
    #NASA MARS NEWS
    url_nasa='https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'

    browser.visit(url_nasa)
    time.sleep(3)
    
    html=browser.html
    soup=bs(html,"html.parser")
    
    # Scrape latest News Title and Paragraph Text.
    article=soup.find("div",class_='list_text')
    news_title=article.find('div',class_="content_title").text
    news_p=article.find('div',class_="article_teaser_body").text

    mars_data["news_title"]=news_title
    mars_data["news_paragraph"]=news_p
    
    #JPL IMAGE
    
    #Visit website to obtain JPL Featured Space Image.
    img_url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(img_url)
    time.sleep(3)
    
    #click on 'FULL IMAGE'
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)

    #click 'more info'
    browser.click_link_by_partial_text('more info')

    #parse HTML from webpage as beautiful soup object
    html=browser.html
    img_soup=bs(html,'html.parser')

    #scrape the url

    img_url=img_soup.find('figure',class_='lede').a['href']
    featured_image_url=f"https://www.jpl.nasa.gov{img_url}"
    
    mars_data["featured_img_url"]= featured_image_url
    
    #MARS WEATHER
    #visit twitter page
    twitter_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    #parse HTML as Beautiful Soup object
    html = browser.html
    soup = bs(html,"html.parser")
    
    #scrape weather from latest tweet
    mars_weather=soup.find('p',class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
    
    mars_data["mars_weather"]=mars_weather
    ###MARS FACTS
    
    #Visit Mars Facts webpage 
    facts_url='https://space-facts.com/mars/'
    browser.visit(facts_url)
    html=browser.html
    
    #Use pandas to scrape the table with the information about Mars from website
    table=pd.read_html(facts_url)
    mars_facts=table[0]
    
    #Rename columns
    mars_facts.columns=['Description','Value']

    #Reset Index 
    mars_facts.set_index('Description')
    
    #Use pandas to convert the data to a HTML table string
    mars_facts=mars_facts.to_html()
    
    mars_data["mars_facts"]=mars_facts
    
    #MARS HEMISPHERES
    
    #visit USGS webpage for Mars hemispheres images
    USGS_url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

    browser.visit(USGS_url)
    html=browser.html

    #parse HTML as Beautiful Soup Object
    soup=bs(html,"html.parser")
    
    #create an dictionary to store titles and image urls
    hemisphere_dict=[]

    #Scrape all elements that have stored information
    result_list=soup.find("div",class_="result-list")
    hemispheres=result_list.find_all("div",class_="item")
    
    
    #Iterate through hemispheres and append to dictionary
    for hemisphere in hemispheres:
        title=hemisphere.find("h3").text
        #Removed Enhanced from each scraped title
        title=title.replace("Enhanced","")
        link=hemisphere.find("a")["href"]
        img_link="https://astrogeology.usgs.gov/"+ link
        browser.visit(img_link)
        html=browser.html
        soup=bs(html,"html.parser")
        downloads=soup.find("div",class_="downloads")
        img_url=downloads.find("a")["href"]
        hemisphere_dict.append({"title":title,"img_url":img_url})

    #Add data into a dictionary
    mars_data={
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url":featured_image_url,
        "mars_weather":mars_weather,
        "mars_facts":mars_facts,
        "hemisphere_image_urls":img_url
        }
    #Close the browser after scraping process is complete
    browser.quit()
    
    
    #Return results
    return mars_data

if __name__=="__main__":
    mars_data=scrape()
    print(f"Here is the scraped information:{mars_data}")
