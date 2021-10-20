import requests
import json
import pprint

from fake_useragent import UserAgent

ua = UserAgent()
INCREMENTED_BY = 12
offset = 0
book_scrape = []
def scraper(offset = 0):
    url = "https://openlibrary.org/subjects/picture_books.json?limit=12&offset=12"

    payload = "limit=12&offset=pageNumber"
    headers = {
    'Content-Type': 'application/json',
    'User-Agent': ua.random
    }

    response = requests.get(url, headers=headers, data=json.dumps(payload))

    data = response.json()
    # pprint.pprint(data)
    works = data['works']
    for book_info in works:
        authors = book_info['title']
        subject = book_info['subject']
        
        pr = {
            'title': authors,
            'subject': subject
        }
        print(pr)
        book_scrape.append(pr)
        
    pageNumber += 1
    scraper(pageNumber=pageNumber)
    
scraper()
print(book_scrape)        

