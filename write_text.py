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


def write_poems(base_url,output_file_path):
 urls=get_urls(base_url)
 # URL of the page containing the HTML text
 for iter, url in enumerate(urls):
  # Fetch the HTML content
  response = requests.get(url)
  response.raise_for_status()  # Ensure the request was successful
  # Parse the HTML content
  soup = BeautifulSoup(response.text, 'html.parser')
  # Find the input element containing the HTML text
  input_element = soup.find('input', {'id': 'HtmlRawText'})
  # Get the HTML content from the 'data-html' attribute
  html_content = input_element['data-html']
  # Decode the HTML entities
  decoded_html = html.unescape(html_content)
  # Parse the decoded HTML content
  parsed_html = BeautifulSoup(decoded_html, 'html.parser')
  # Extract text content, maintaining the line structure
  lines = []
  for p_tag in parsed_html.find_all('p'):
    line_text = ''.join(span.get_text() for span in p_tag.find_all('span'))
    lines.append(line_text)
  # Join lines with newline characters
  concatenated_text = '\n'.join(lines)
  f=open(output_file_path,'a')
  f.write(concatenated_text)
  f.close()
 print('writing complete')
 return
