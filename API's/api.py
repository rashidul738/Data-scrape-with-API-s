from sqlite3.dbapi2 import OperationalError
import requests
import json
import sqlite3
from fake_useragent import UserAgent
from urllib.parse import urljoin

ua = UserAgent()

extracted_product = []

def scraper(PageNumber=1):
  url = "https://www.walgreens.com/productsearch/v3/products/search"
  
  # querystring = {"instart_disable_injection":"true"}

  payload = {"p":PageNumber,"s":72,"view":"allView","geoTargetEnabled":False,"abtest":["tier2","showNewCategories"],"deviceType":"desktop","id":["360457"],"requestType":"tier3","source":"rootTier3","sort":"Top Sellers","couponStoreId":"15196","storeId":"15196"}
  headers = {
    'Content-Type': 'application/json',
    'User-Agent': ua.random,
    'Cookie': '_abck=03554634A438DE00AA5B79A148C87C18~-1~YAAQnJYRYG/3mLV6AQAAEghr/AY5bZu4q0Y/EUvW2G9OLiqEahYX1qM4I+YpS6Z3cxzTzwvH3oPSHOhv/yYmiYTEtvoAwZRA9+B81WNw2710ovV2DVua4MiXseFL14jaN27M6fjzQNBdh9Y4A8B8NHNYQDWiGDUkDMbluD6D+CplTPLaQjLe9qbSEX3q9w2KoSlck7nPT45TcX1NELSmgyu8d/aZDeyF+dRaf0BN3OZ2WNSWxMerzPAgx9MdPGALJyDTi2htoEUbl4K7xHa8UAN1Di/FjlIQbwzS/DbkD/xeyN3h6vJey4mrgwwwkPdfR77Om8U1TG0aaiOwx6fqRp8bLA/RlSc/t31HVasERzIqUajMBOZXt5K8H4Ev2Hs8lnX6rvUwI408bSfW4EK6bV+JM8EzbqUMX5PV~0~-1~-1; Domain=.walgreens.com; Path=/; Expires=Sun, 31 Jul 2022 11:55:10 GMT; Max-Age=31536000; Secure'
  }

  response = requests.post(url, data=json.dumps(payload), headers=headers)

  data = response.json()

  try:
    products = data['products']
    
    
    for product_info in products:
      pr_info = product_info['productInfo']
      pr = {
        'Catagory_Name': pr_info['beautyCategoryName'],
        'productName': pr_info['productName'],
        'productPrice': pr_info['priceInfo']['regularPrice'],
        'productSize': pr_info['productSize'],
        'productType': pr_info['productType'],
        'productURL': urljoin(base='https://www.walgreens.com', url=pr_info['productURL']),
        'imageUrl': urljoin(base='https://www.walgreens.com', url=pr_info['imageUrl']),
        'prodId': pr_info['prodId'],
        'skuId': pr_info['skuId']
      }
      extracted_product.append(pr)


    PageNumber += 1
    scraper(PageNumber=PageNumber)
  except KeyError:
    return
  
  
scraper()

connection = sqlite3.connect("walgreens.db")
c = connection.cursor()
try:
  c.execute('''
            CREATE TABLE products (
              skuId TEXT PRIMARY KEY,
              Catagory_Name TEXT,
              productName TEXT,
              productPrice TEXT,
              productSize TEXT,
              productType TEXT,
              productURL TEXT,
              imageUrl TEXT,
              prodId TEXT
            )
            ''')

  connection.commit()
except sqlite3.OperationalError as e:
  print(e)

for product in extracted_product:
  try:
    c.execute('''
              INSERT INTO products (skuId, Catagory_Name, productName, productPrice, productSize, productType, productUrl, imageUrl, prodId) VALUES(
                ?,?,?,?,?,?,?,?,?
              )
          ''',(
            product['skuId'],
            product['Catagory_Name'],
            product['productName'],
            product['productPrice'],
            product['productSize'],
            product['productType'],
            product['productURL'],
            product['imageUrl'],
            product['prodId']
          )
    )
  except sqlite3.IntegrityError:
    pass  
  
connection.commit()
connection.close()  



