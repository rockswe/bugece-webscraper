from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import json
import time

# path to ChromeDriver executable
chrome_service = Service("/opt/homebrew/bin/chromedriver")  # in this case, it's for ChromeDriver installed by homebrew on MacOS (Silicon M3)
driver = webdriver.Chrome(service=chrome_service)

# navigate to the events page
driver.get("https://bugece.co/en/events")
time.sleep(5)  # allow the page to load completely

# scroll through the page to load all events
for _ in range(15):  # adjust range for the total number of events
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)

# find all event cards
event_cards = driver.find_elements(By.CSS_SELECTOR, "div.mb-4.px-3.col-xl-3.col-lg-3.col-md-4.col-6")
print(f"Found {len(event_cards)} event cards.")

# list to store extracted event details
events = []

# process each card
for card in event_cards:
    try:
        # extract title
        try:
            title_element = card.find_element(By.CSS_SELECTOR, "div[data-css-19da2xt] span")
            title = title_element.text.strip()
        except:
            title = "N/A"

        # extract event link
        try:
            link_element = card.find_element(By.TAG_NAME, "a")
            event_link = link_element.get_attribute("href")
        except:
            event_link = "N/A"

        # extract image URL
        try:
            img_element = card.find_element(By.TAG_NAME, "img")
            image_url = img_element.get_attribute("src")
        except:
            image_url = "N/A"

        # extract date
        try:
            date_element = card.find_element(By.CSS_SELECTOR, "span[data-css-1ondyc7] time")
            event_date = date_element.text.strip()
        except:
            event_date = "N/A"

        # extract start and end time
        try:
            time_elements = card.find_elements(By.CSS_SELECTOR, "div[data-css-1ozg4x2] span")
            start_time = time_elements[0].text.strip() if len(time_elements) > 0 else "N/A"
            end_time = time_elements[1].text.strip() if len(time_elements) > 1 else "N/A"
        except:
            start_time, end_time = "N/A", "N/A"

        # extract location
        try:
            location_element = card.find_element(By.CSS_SELECTOR, "span[data-css-ul2y7h]")
            location = location_element.text.strip()
        except:
            location = "N/A"

        # append the event data
        events.append({
            "title": title,
            "link": event_link,
            "image_url": image_url,
            "date": event_date,
            "start_time": start_time,
            "end_time": end_time,
            "location": location,
        })
    except Exception as e:
        print(f"Error processing card: {e}")

# quit the browser
driver.quit()

# save the results to events.JSON
output_file = "events.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(events, f, ensure_ascii=False, indent=4)

print(f"scraped event data saved to {output_file}.")
