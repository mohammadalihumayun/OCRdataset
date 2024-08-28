
import sys
sys.path.insert(0,'/usr/lib/chromium-browser/chromedriver')

import csv
import time
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
#import chromedriver_autoinstaller
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_poem_urls(url) # e.g. url = "https://www.rekhta.org/poets/allama-iqbal/ghazals?lang=ur"

 # setup chrome options
 chrome_options = webdriver.ChromeOptions()
 chrome_options.add_argument('--headless') # ensure GUI is off
 chrome_options.add_argument('--no-sandbox')
 chrome_options.add_argument('--disable-dev-shm-usage')
 driver = webdriver.Chrome(options=chrome_options)

 # Step 2: Open the page
 driver.get(url)

 # Step 3: Scroll down to load all content
 SCROLL_PAUSE_TIME = 2

 # Get scroll height
 last_height = driver.execute_script("return document.body.scrollHeight")

 while True:
    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    time.sleep(SCROLL_PAUSE_TIME)

    # Calculate new scroll height and compare with last scroll height
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

 # Step 4: Get page source and parse with BeautifulSoup
 html_content = driver.page_source
 soup = BeautifulSoup(html_content, 'html.parser')

 # Step 5: Find all <div> elements with class 'contentListItems nwPoetListBody'
 divs = soup.find_all('div', class_='contentListItems nwPoetListBody')

 # Step 6: Extract the URLs from the <a> elements within each <div>
 urls = []
 for div in divs:
    a_tag = div.find('a', href=True)
    if a_tag:
        urls.append(a_tag['href'])

 # Step 7: Print the extracted URLs
 for url in urls:
    print(url)

 # Close the browser
 driver.quit()
 return urls
