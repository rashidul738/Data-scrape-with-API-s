from os import replace
import sqlite3
import requests
from fake_useragent import UserAgent

ua = UserAgent()

quotes_scrape =[]


for i in range(1,11):
  url = f"http://quotes.toscrape.com/api/quotes?page={i}"

  payload = ""

  headers = {
    'Content-Type': 'application/json',
    'User-Agent': ua.random
  }

  response = requests.get(url, headers=headers, data=payload)

  data = response.json()

  quotes = data['quotes']
  for quote_info in quotes:
    
    
    pr = {
      'author': quote_info['author']['name'],
      'tags': quote_info['tags'],
      'text': quote_info['text']
    }
    quotes_scrape.append(pr)

connection = sqlite3.connect("quotes.db")
c = connection.cursor()
try:
  c.execute('''
            CREATE TABLE quotes (
              author TEXT PRIMARY KEY,
              tags TEXT,
              text TEXT
            )
            ''')
  connection.commit()
except sqlite3.OperationalError as e:
  print(e)

for quote in quotes_scrape:
  c.execute('''
            INSERT INTO quotes (author, tags, text) VALUES(
              ?,?,?
            )
        ''',(
            quote['author'],
            quote['tags'],
            quote['text']
          )
    )
  connection.commit()
  connection.close()
