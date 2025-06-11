import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import pandas as pd

def scrape_google_maps(query, num_scrolls=5):
    """
    Scrapes Google Maps for business information based on a search query.

    Args:
        query (str): The search query (e.g., "restaurants in New York").
        num_scrolls (int): The number of times to scroll to load more results.
    """
    # Setting up Chrome options
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode (without GUI)
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu") # This is often necessary for headless on Linux

    # Set up chromedriver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        # Open Google Maps
        driver.get("https://www.google.com/maps")
        time.sleep(3)  # Wait for the page to load

        # Find the search box and enter the query
        search_box = driver.find_element(By.ID, "searchboxinput")
        search_box.send_keys(query)
        search_box.send_keys(Keys.ENTER)
        time.sleep(5)  # Wait for search results to load

        # Scroll to load more results
        # Updated XPath for the scrollable element
        scrollable_element_xpath = '//*[@role="feed"]'
        try:
            results_list = driver.find_element(By.XPATH, scrollable_element_xpath)
        except:
            print("Could not find the scrollable element. Trying a more general approach.")
            # Fallback to body or html if the specific pane is not found
            results_list = driver.find_element(By.TAG_NAME, "body")


        for i in range(num_scrolls):
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", results_list)
            time.sleep(3) # Wait for content to load after scroll

        # Get the page source after scrolling
        page_source = driver.page_source

        # Parse with BeautifulSoup
        soup = BeautifulSoup(page_source, "html.parser")

        # Find all the relevant data containers
        # Updated class names for the results
        data_containers = soup.find_all("div", class_="Nv2PK THOPZb CpccDe")

        results = []
        for container in data_containers:
            name_tag = container.find("div", class_="qBF1Pd fontHeadlineSmall")
            address_tag = container.find("span", class_="W4Efsd")
            rating_tag = container.find("span", class_="MW4etd")

            name = name_tag.text.strip() if name_tag else "N/A"
            address = address_tag.text.strip() if address_tag else "N/A"
            rating = rating_tag.text.strip() if rating_tag else "No rating"

            results.append({"name": name, "address": address, "rating": rating})

        # Create a DataFrame and save to CSV
        if results:
            df = pd.DataFrame(results)
            output_filename = f"google_maps_scrape_{query.replace(' ', '_').replace('/', '_')}.csv"
            df.to_csv(output_filename, index=False, encoding='utf-8')
            print(f"Scraping complete. Data saved to {output_filename}")
        else:
            print("No results found or extracted.")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit() # Ensure the browser is closed

if __name__ == "__main__":
    search_query = input("Enter your search query for Google Maps (e.g., 'restaurants in New York'): ")
    scroll_count = int(input("Enter number of scrolls (e.g., 5 for more results): "))
    scrape_google_maps(search_query, scroll_count) 