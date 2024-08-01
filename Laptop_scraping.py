from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

# Initialize the WebDriver with the Service object
chrome_options = Options()
chrome_options.add_argument("--disable-search-engine-choice-screen")
driver = webdriver.Chrome(options=chrome_options)
driver.implicitly_wait(10)

def slow_scroll_to_bottom():
    """Slowly scroll to the bottom of the page to load dynamic content."""
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollBy(0, 200);")  # Scroll down by 500 pixels
        time.sleep(0.5)  # Wait for a short period to allow new content to load
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

def get_page_html(page_number):
    url = f"https://www.flipkart.com/search?q=laptop&otracker=search&otracker1=search&marketplace=FLIPKART&as-show=off&as=off&page={page_number}"
    driver.get(url)
    slow_scroll_to_bottom()  # Scroll to the bottom to load all dynamic content
    return driver.page_source

try:
    # Define the number of pages you want to scrape
    num_pages = 85
    all_html = ""

    for page_number in range(2, num_pages + 1):
        print(f"Scraping page {page_number}...")
        page_html = get_page_html(page_number)
        all_html += page_html
        
        # Optionally, you can add a sleep period to avoid being flagged for too many requests in a short time
        time.sleep(3)  # Wait for a bit before moving to the next page

    # Save the combined HTML content to a file
    with open("scrapped_Laptop_data.txt", "w", encoding="utf-8") as file:
        file.write(all_html)

finally:
    # Ensure the driver is closed properly
    driver.quit()
