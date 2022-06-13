from fileinput import filename
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from datetime import date
import re
from time import sleep
import json
from serpapi import GoogleSearch
import requests


today = date.today()
d = today.strftime("%B %d, %Y")

# search = input("Enter item to be searched: ")

with open('Product names.json', 'r') as Products:
    names = json.load(Products)
    company = list(names)
    prod = list(names.values())


geoBlocked = webdriver.FirefoxOptions()
geoBlocked.set_preference("geo.prompt.testing", True)
geoBlocked.set_preference("geo.prompt.testing.allow", False)

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36',
    'Accept-Language': 'en-US, en;q=0.5'
}


# -----------------
#       Amazon
# -----------------

def AmazonScraper(search, items):
    count = 0

    # with open('regions.json', 'r') as url_file:
    #    file_url = json.load(url_file)
    #   loc = list(file_url)
    #  urls = list(file_url.values())

    # search = 'Microsoft 365'
    search_query = search.replace(' ', '+')

    url = "https://www.amazon.com/"
    # for url in urls:
    base_url = url + 's?k={0}'.format(search_query)
    # file_name = company[company_number] + ' Amazon ' + loc[count] + ' ' + d

    print('Page {0} ...'.format(base_url + '&page=1'))
    response = requests.get(
        base_url + '&page=1', headers=headers)
    soup = BeautifulSoup(response.content, 'lxml')

    results = soup.find_all(
        'div', {'class': 's-result-item', 'data-component-type': 's-search-result'})

    for result in results:
        product_name = result.h2.text

        # if re.search(search + '*', product_name):
        try:
            price = result.find(
                'span', {'class': 'a-offscreen'}).text
            product_url = url + result.h2.a['href']
            items.append([product_name, price, product_url])
        except AttributeError:
            continue
            # else:
            # continue
    sleep(1.5)

    name = 'Amazon USA '
    count = count + 1
    return name


# -----------------
#     BEST BUY
# -----------------


# FIX SO THAT IT DOESNT OPEN BROWSER EVERY SINGLE TIME IT HAS TO MAKE A SEARCH
def BestBuyScraper(search, items):

    srch_fn = browser.find_element_by_id('gh-search-input')
    srch_fn.send_keys(search)

    sleep(1.5)

    search_button = browser.find_element_by_class_name('header-search-icon')
    search_button.click()

    page_src = browser.page_source

    soup = BeautifulSoup(page_src, 'lxml')

    results = soup.find_all('li', {'class': 'sku-item'})

    url = 'https://www.bestbuy.com'

    for result in results:
        product_name = result.h4.text
        try:
            price = result.find(
                'div', {'class': 'priceView-hero-price'}).text
            price = '$' + re.search(r"\d+\.\d+", price)[0]
            product_url = url + result.h4.a['href']
            items.append([product_name, price, product_url])
        except AttributeError:
            continue
        sleep(1.5)

    name = 'BestBuy '
    browser.back()
    return name

# -----------------
#       HP
# -----------------


def HPScraper():

    count = 0

    links = {
        "HP Omen": 'https://www.hp.com/us-en/shop/ConfigureView?langId=-1&storeId=10151&catalogId=10051&catEntryId=3074457345619993322&urlLangId=&quantity=1',
        "HP Spectre": 'https://www.hp.com/us-en/shop/ConfigureView?langId=-1&storeId=10151&catalogId=10051&catEntryId=3074457345620102827&urlLangId=&quantity=1'
    }

    items = []

    urls = list(links.values())
    names = list(links)

    for link in urls:
        browser = webdriver.Firefox(options=geoBlocked)
        browser.get(link)
        page_src = browser.page_source

        soup = BeautifulSoup(page_src, 'lxml')

        results = soup.find_all('div', {'class': 'configure-option'})
        for result in results:
            for cat in result:
                for sub_cat in cat:
                    try:
                        price = sub_cat.find(
                            'div', {'class': 'radio-info price'}).text
                        price = price.replace('+', '').lstrip()
                        name = sub_cat.find(
                            'div', {'class': 'radio-label'}).text
                    except:
                        continue
                    items.append([name, price, names[count], link])

        results = soup.find_all(
            'div', {'class': 'configure-option', 'data-path': "39R27AV.CreatorSoftware"})
        for result in results:
            for cat in result:
                try:
                    name = cat.find(
                        'span', {'class': "Checkbox-module_content__3j9aq"}).text
                    price = cat.find(
                        'div', {'class': "PriceBlock-module_salePrice___Hf7T"}).text
                    name = name.replace(price, "")
                except:
                    continue
                items.append([name, price, names[count], link])

        browser.quit()

        item_req = [
            item for item in items for app in company if app in item[0]]

        file_name = names[count] + ' ' + d
        df = pd.DataFrame(item_req, columns=[
                          'product', 'price', 'HP Product name', 'url'])
        df.to_json('{0}.json'.format(file_name), orient='records')
        count = count + 1


# -----------------
#      Lenovo
# -----------------


def LenovoScraper():
    link = "https://www.lenovo.com/us/en/configurator/cto/index.html?bundleId=82BJCTO1WWUS1"

    browser = webdriver.Firefox(options=geoBlocked)
    browser.get(link)

    sleep(2)

    button1 = browser.find_element_by_xpath(
        '//*[contains(concat( " ", @class, " " ), concat( " ", "common_step_bar_content", " " )) and (((count(preceding-sibling::*) + 1) = 3) and parent::*)]//*[contains(concat( " ", @class, " " ), concat( " ", "common_step_bar_num_text_status", " " ))]')

    button1.click()

    page_src = browser.page_source

    soup = BeautifulSoup(page_src, 'lxml')

    results = soup.find_all(
        'div', {'class': 'section_list soft_ware_sections'})
    print(results)


# -----------------
#      Walmart
# -----------------


def WalmartScraper(search, items):
    engine = "walmart"

    params = {
        "api_key": "dd8a3a3e696b0c8ab7db5cbb3952bc2577623e3d5ec49a08e0076fd7a136da85",
        "engine": engine,
        "query": search
    }

    search = GoogleSearch(params)
    results = search.get_dict()

    for result in results["organic_results"]:
        product_title = result['title']
        product_link = result['product_page_url']
        offer = result['primary_offer']
        price = offer['offer_price']

        items.append({
            'product': product_title,
            'link': product_link,
            'price': price
        })

    name = 'Walmart '
    return name


def file_writer(items, company_number, nm):
    res = [i for n, i in enumerate(items) if i not in items[n + 1:]]
    df = pd.DataFrame(res, columns=['product', 'price', 'product url'])
    file_name = nm + company[company_number] + ' ' + d
    df.to_json('{0}.json'.format(file_name), orient='records')


company_number = 0

for item in prod:
    items = []
    browser = webdriver.Firefox(options=geoBlocked)

    browser.get('https://www.bestbuy.com/site')

    eng = browser.find_element_by_class_name("us-link")
    eng.click()

    print("Best Buy USA")

    for search in item:
        nm1 = BestBuyScraper(search, items)
    file_writer(items, company_number, nm1)
    company_number = company_number + 1
    browser.quit()

company_number = 0

for item in prod:
    items = []
    for search in item:
        nm1 = AmazonScraper(search, items)
    file_writer(items, company_number, nm1)
    company_number = company_number + 1

company_number = 0

for item in prod:
    items = []
    for search in item:
        nm1 = WalmartScraper(search, items)
    file_writer(items, company_number, nm1)
    company_number = company_number + 1


# BestBuyScraper(search)

HPScraper()
# LenovoScraper()
