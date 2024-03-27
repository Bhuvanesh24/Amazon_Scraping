from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

# Function to extract Product Title
def get_title(soup):
    title = soup.find("span", attrs={"id":'productTitle'})
    return title.text.strip() if title else ""

# Function to extract Product Price
def get_price(soup):
    price = soup.find("span", attrs={'id':'priceblock_ourprice'})
    if price:
        return price.text.strip()
    else:
        deal_price = soup.find("span", attrs={'id':'priceblock_dealprice'})
        return deal_price.text.strip() if deal_price else ""

# Function to extract Product Rating
def get_rating(soup):
    rating = soup.find("i", attrs={'class':'a-icon a-icon-star'})
    return rating.text.strip() if rating else ""

# Function to extract Number of User Reviews
def get_review_count(soup):
    review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'})
    return review_count.text.strip() if review_count else ""

# Function to extract Availability Status
def get_availability(soup):
    availability = soup.find("div", attrs={'id':'availability'})
    return availability.text.strip() if availability else "Not Available"

if __name__ == '__main__':
    # Add your user agent 
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

    # The webpage URL
    URL = "https://www.amazon.in/s?k=bags&crid=2M096C61O4MLT&qid=1653308124&sprefix=ba%2Caps%2"

    # HTTP Request
    webpage = requests.get(URL, headers=HEADERS)

    # Soup Object containing all data
    soup = BeautifulSoup(webpage.content, "html.parser")

    # Fetch links pointing to product pages
    links = soup.select("a.a-link-normal.a-text-normal[href^='/dp/']")

    d = {"title":[], "price":[], "rating":[], "reviews":[],"availability":[]}

    # Loop for extracting product details from each link
    for link in links:
        product_url = "https://www.amazon.in" + link['href']
        new_webpage = requests.get(product_url, headers=HEADERS)
        new_soup = BeautifulSoup(new_webpage.content, "html.parser")

        # Function calls to display all necessary product information
        d['title'].append(get_title(new_soup))
        d['price'].append(get_price(new_soup))
        d['rating'].append(get_rating(new_soup))
        d['reviews'].append(get_review_count(new_soup))
        d['availability'].append(get_availability(new_soup))

    amazon_df = pd.DataFrame.from_dict(d)
    amazon_df['title'] = amazon_df['title'].replace('', np.nan)
    amazon_df.dropna(subset=['title'], inplace=True)
    amazon_df.to_csv("amazon_data.csv", header=True, index=False)
