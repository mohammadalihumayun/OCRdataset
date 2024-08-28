### web text scraping
"""text scraping"""


import requests
from bs4 import BeautifulSoup
import html

def get_urls(url):
 #url = "https://www.rekhta.org/poets/allama-iqbal/ghazals?lang=ur"
 #url='https://www.rekhta.org/poets/allama-iqbal/nazms?lang=ur'
 #Genre='Nazms'#Ghazals'

 # Step 1: Fetch the HTML content of the page
 response = requests.get(url)
 html_content = response.content

 # Step 2: Parse the HTML content using BeautifulSoup
 soup = BeautifulSoup(html_content, 'html.parser')

 # Step 3: Find all <div> elements with class 'contentListItems nwPoetListBody'
 divs = soup.find_all('div', class_='contentListItems nwPoetListBody')

 # Step 4: Extract the URLs from the <a> elements within each <div>
 urls = []
 for div in divs:
    a_tag = div.find('a', href=True)
    if a_tag:
        urls.append(a_tag['href'])

 #for url in urls:
 #    print(url)

 print('urls fetched: ',len(urls))
 return urls
