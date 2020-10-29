from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import logging
import time
import pandas as pd
import sqlite3
import Inputhandler

# initializing logging file
logging.basicConfig(format='%(asctime)s: %(levelname)s:%(message)s', filename='amazon.log', level=logging.INFO)

# setting options for chrome driver
options = Options()
# options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument('--disable-infobars')
options.add_argument('--start-fullscreen')
options.add_argument("--disable-popup-blocking")


def info(msg1='', msg2='', msg3=''):
    logging.info(str(msg1) + str(msg2) + str(msg3))
    print(msg1, msg2, msg3)


info("<amazon>  trying to connecting to url", ' at ', time.ctime())

url = "https://www.amazon.in/s?k=mobiles&ref=nb_sb_noss_2"
driver = webdriver.Chrome(chrome_options=options)
driver.get(url)

header = "(//h2)[{}]"
rating = "(//h2/following::span[@class='a-icon-alt'])[{}]"
price = '(//span[@class="a-price-whole"])[{}]'
r = []
h = []
p = []
t = []

for i in range(1, 26):
    header_path = header.format(i)
    h.append(Inputhandler.readText(driver, header_path))
    xpath_rating = rating.format(i)
    r.append(Inputhandler.getAttribute(driver, xpath_rating, "innerHTML"))
    xpath_price = price.format(i)
    p.append(Inputhandler.readText(driver, xpath_price))
    t.append(time.ctime())
dff = pd.DataFrame({'Header': h, 'rating': r, 'price': p, 'time': t})

driver.close()
dff

conn = sqlite3.connect('amazon.db')

c = conn.cursor()


def create_table():
    c = conn.cursor()
    c.execute('CREATE TABLE IF NOT EXISTS AmazonPriceList(header TEXT, rating TEXT,price REAL, timestamp TEXT)')
    c.close()


def dynamic_data_entry(header, rating, price, _time):
    c = conn.cursor()
    c.execute('INSERT INTO AmazonPriceList (header,rating,price,_time ) VALUES(?,?,?,?)',
              (header, rating, price, _time))
    conn.commit()
    c.close()
