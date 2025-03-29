from bs4 import BeautifulSoup
import time
import random
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException, NoSuchElementException




BASE_URL = "https://skinport.com/de/market?"
EDGEDRIVER_PATH = './msedgedriver.exe'

edge_options = EdgeOptions()
edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--window-size=1920,1080")
edge_options.add_argument("--log-level=3")
edge_options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0")

service = EdgeService(executable_path=EDGEDRIVER_PATH)

def get_skin_price(item_identifier):
    """ 
    Fetches and parses lowest price for a specific item from Skinport using Selenium and Edge

    Args:
        item_identifier (str): The unique string (from config.json) that
                               identifies the item on Skinport. This is
                               often the URL-encoded market_hash_name.

    Returns:
        float: The lowest price found for the item, as a float.
        None: If the price could not be found or an error occurred.

    """
    target_url = f"{BASE_URL}{item_identifier}"

    print(f"Attempting to fetch: {target_url}")

    driver = None

    try:
        driver = webdriver.Edge(service=service, options=edge_options)
        driver.get(target_url)

        listing_container_selector = '.CatalogPage-items'
        listing_item_selector = '.CatalogPage-item.CatalogPage-item--grid'
        wait_time = 20
        print(f"Waiting up to {wait_time}s for listing container '{listing_container_selector}'...")
        WebDriverWait(driver, wait_time).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, listing_item_selector))
        )

        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')
        listing_elements = soup.select(listing_item_selector)


        if not listing_elements:
                print(f"Warning: No listing elements found for identifier: {item_identifier} at URL: {target_url}")
                return None
    
        prices = []
        for element in listing_elements:
             price_tag = element.find('div.Tooltip-link')

    except TimeoutException:    
        print(f"Error: Timed out waiting for elements for {item_identifier} at {target_url}")
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



