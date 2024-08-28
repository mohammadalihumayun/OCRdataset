import requests
from bs4 import BeautifulSoup
import html

def write_poems(output_file_path):

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
