import requests
from bs4 import BeautifulSoup
import time
import random

BASE_URL = "https://skinport.com/de/market?"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
}

def get_skin_price(item_identifier):
    """ 
    Scrapes and parses price for specific skin from skinport.

    Args:
        item_identifier (str): Unique string from config.json that identifies
        the item on skinport.

    Returns:
        float: The lowest price found for the item, as a float.
        None: If price could not be found (network error, page structure changed, item not listed).

    """
    target_url = f"{BASE_URL}{item_identifier}"

    print(f"Attempting to fetch: {target_url}")

    try:
        response = requests.get(target_url, headers=HEADERS, timeout=20)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        listing_elements = soup.select('.CatalogPage-item.CatalogPage-item--grid')

        if not listing_elements:
                print(f"Warning: No listing elements found for identifier: {item_identifier} at URL: {target_url}")
                return None
    
        prices = []
        for element in listing_elements:
             price_tag = element.find('div.Tooltip-link')

    except requests.exceptions.RequestException as e:    
        print(f"Error fetching URL {target_url}: {e}")
        return None

if __name__ == "__main__":
     
     print("--- Starting Scraper Test ---")

     test_identifier = "cat=Knife&item=Black+Laminate&type=Karambit&exterior=5"

     price = get_skin_price(test_identifier)

     if price is not None:
        print(f"\n---> Success! Lowest price found!: {price}" )
     else:
        print("\nFailed to retrieve price. Check log for errors.")

print("--- Scraper Test Finished ---")



