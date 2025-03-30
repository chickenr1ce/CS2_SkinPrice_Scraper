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




BASE_URL = "https://gamerpay.gg/?query="
EDGEDRIVER_PATH = './msedgedriver.exe'

edge_options = EdgeOptions()
#edge_options.add_argument("--headless")
edge_options.add_argument("--disable-gpu")
edge_options.add_argument("--window-size=1920,1080")
edge_options.add_argument("--log-level=3")
edge_options.add_argument(f"user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0")

service = EdgeService(executable_path=EDGEDRIVER_PATH)

def get_skin_price(item_identifier):
    """ 
    Fetches and parses lowest price for a specific item from CSFloat using Selenium and Edge

    Args:
        item_identifier (str): The unique string (from config.json) that
                               identifies the item on CSFloat. This is
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

        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

        driver.get(target_url)

        # --- COOKIE HANDLING ---

        cookie_wait_time = 10
        accept_button_selector = 'CookiePopup-button'

        try:        
            print(f"Waiting up to {cookie_wait_time}s for cookie accept button...")
            accept_button = WebDriverWait(driver, cookie_wait_time).until(
                EC.element_to_be_clickable((By.CLASS_NAME, accept_button_selector))
            )  

            print("Cookie accept button found. Clicking...")
            accept_button.click()
            print("Cookie button clicked")

            time.sleep(1)

        except TimeoutException:
            print("Cookie accept button not found or timed out. Proceeding anyway.")
        
        except Exception as cookie_e:
            print(f"Error handling cookie button: {cookie_e}. Proceeding anyway.")

        #--- END OF COOKIE HANDLING --- 

        listing_container_selector = '<ng-tns-c2422869881-16'
        listing_item_selector = 'CatalogPage-item'
        wait_time = 20

        print(f"Waiting up to {wait_time}s for listing container '{listing_container_selector}'...")
        WebDriverWait(driver, wait_time).until(EC.presence_of_all_elements_located((By.CLASS_NAME, listing_container_selector))
        )

        time.sleep(1.5)

        print(f"Waiting up to {wait_time}s for listing items '{listing_item_selector}'...")
        WebDriverWait(driver,wait_time).until(EC.presence_of_all_elements_located((By.CLASS_NAME,listing_item_selector))
        )

        print("Listings appear to have loaded.")

        html_content = driver.page_source

        soup = BeautifulSoup(html_content, 'html.parser')
        listing_elements = soup.select(listing_item_selector)


        if not listing_elements:
                print(f"Warning: No listing elements found for identifier: {item_identifier} at URL: {target_url}")
                return None
    
        prices = []

        price_tag_selector = 'div.Tooltip-link'

        print(f"Found {len(listing_elements)} listing elements. Extracting prices...")

    except TimeoutException:    
        print(f"Error: Timed out waiting for elements for {item_identifier} at {target_url}")
        
        try:
            screenshot_path = f'timeout_screenshot_{item_identifier}.png'
            driver.save_screenshot(screenshot_path)
            print(f"Screenshot saved to {screenshot_path}")
        except Exception as screen_e:
            print(f"Could not save screenshot: {screen_e}")
        return None

if __name__ == "__main__":
     
     print("--- Starting Scraper Test ---")

     test_identifier = "karambit+black+laminate&wear=Well-Worn&page=1"

     price = get_skin_price(test_identifier)

     if price is not None:
        print(f"\n---> Success! Lowest price found!: {price}" )
     else:
        print("\nFailed to retrieve price. Check log for errors.")

print("--- Scraper Test Finished ---")



