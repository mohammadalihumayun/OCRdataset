# Required Instllations
```
pip install PyPDF2
pip install pdf2image
apt-get install poppler-utils
```

# Running the script:

To scrap poetry text from web
```
python fetch.py --base_url http://example.com --out_file poems.txt
```
To segment sentence images from pdf file
```
python fetch.py --pdf_path document.pdf --output_path segmented_images --start_page 1 --stop_page 5
```
