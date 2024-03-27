import requests
from bs4 import BeautifulSoup
import csv
from fake_useragent import UserAgent
from tenacity import retry, stop_after_attempt, wait_fixed
from requests.exceptions import HTTPError
import time


@retry(stop=stop_after_attempt(3), wait=wait_fixed(10), retry_error_callback=lambda x: isinstance(x, HTTPError))
def fetch_url(url):
    user_agent = UserAgent().random  
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response
    else:
        return None


@retry(stop=stop_after_attempt(3), wait=wait_fixed(10), retry_error_callback=lambda x: isinstance(x, HTTPError))
def fetch_product_page(url):
    response = fetch_url(url)
    return response


def scrape_product_page(url):
    additional_info = {}
    response = fetch_product_page(url)
    if response is None:
        print(f"Error occurred while fetching product page {url}")
        return additional_info
    soup = BeautifulSoup(response.text, 'html.parser')
    
    product_desc = soup.find('div', {'id': 'productDescription'})
    if product_desc:
        additional_info['description'] = product_desc.text.strip()
    return additional_info


def scrape_amazon_products(url, num_pages=20, max_products=200):
    all_products = []
    products_scraped = 0

    for page in range(1, num_pages + 1):
        if products_scraped >= max_products:
            break

        page_url = f"{url}&ref=sr_pg_{page}"
        print(f"Scraping page {page}: {page_url}")

        response = fetch_url(page_url)
        if response is None:
            print(f"Error occurred while fetching page {page}")
            continue

        soup = BeautifulSoup(response.text, 'html.parser')
        products = soup.find_all('div', {'data-component-type': 's-search-result'})

        for product in products:
            if products_scraped >= max_products:
                break

            product_info = {}
            
            product_link = product.find('a', {'class': 'a-link-normal'})
            if product_link:
                product_url = "https://www.amazon.in" + product_link['href']
                product_info['url'] = product_url
               
                additional_info = scrape_product_page(product_url)
                product_info.update(additional_info)
                all_products.append(product_info)
                products_scraped += 1

           
            time.sleep(1)

    return all_products


def export_to_csv(data):
    with open('amazon_products.csv', 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = set().union(*(d.keys() for d in data))  
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for product in data:
            writer.writerow(product)


url = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2"


scraped_products = scrape_amazon_products(url)


export_to_csv(scraped_products)

print("Scraping and exporting completed.")
