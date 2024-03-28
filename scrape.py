import requests
from bs4 import BeautifulSoup
import csv

def scrape_product_listings(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    products = soup.find_all("div", class_="s-result-item")
    for product in products:
        product_link = product.find("a", class_="a-link-normal")
        if product_link:
            product_url = "https://www.amazon.in" + product_link.get("href")
            product_name_element = product.find("span", class_="a-size-medium")
            product_name = product_name_element.text.strip() if product_name_element else "Not available"
            product_price_element = product.find("span", class_="a-offscreen")
            product_price = product_price_element.text.strip() if product_price_element else "Not available"
            rating_element = product.find("span", class_="a-icon-alt")
            rating = rating_element.text.split()[0] if rating_element else "Not available"
            num_reviews_element = product.find("span", class_="a-size-base")
            num_reviews = num_reviews_element.text.split()[0] if num_reviews_element else "0"
            scrape_product_details(product_url, product_name, product_price, rating, num_reviews)

def scrape_product_details(product_url, product_name, product_price, rating, num_reviews):
    response = requests.get(product_url)
    soup = BeautifulSoup(response.text, "html.parser")
    description_element = soup.find("div", id="productDescription")
    description = description_element.text.strip() if description_element else "Not available"
    asin_element = soup.find("th", text="ASIN")
    asin = asin_element.find_next_sibling("td").text.strip() if asin_element else "Not available"
    product_description_element = soup.find("div", id="feature-bullets")
    product_description = product_description_element.text.strip() if product_description_element else "Not available"
    manufacturer_element = soup.find("th", text="Manufacturer")
    manufacturer = manufacturer_element.find_next_sibling("td").text.strip() if manufacturer_element else "Not available"
    data.append([product_url, product_name, product_price, rating, num_reviews, description, asin, product_description, manufacturer])

data = []

for page_num in range(1, 21):
    url = f"https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2C283&ref=sr_pg_{page_num}"
    print(f"Scraping page {page_num}")
    scrape_product_listings(url)

with open('amazon_products.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Product URL', 'Product Name', 'Product Price', 'Rating', 'Number of Reviews', 'Description', 'ASIN', 'Product Description', 'Manufacturer'])
    writer.writerows(data)

print("Scraping complete. Data saved to amazon_products.csv")
