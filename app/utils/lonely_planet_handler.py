from httpx import AsyncClient
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import validators

#web scraping to highlight more stereotypical/popular attractions - used to give users additional options aside from the curated iterinary

class LonelyPlanetHandler:

    def __init__(self, location):
        self.location = location
        options = Options()
        options.add_argument("--headless")  
        options.add_argument("--disable-gpu") 
        options.add_argument("--no-sandbox") 
        options.add_argument("--disable-blink-features=AutomationControlled") 
        options.add_argument("--start-maximized") 
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )  

        self.driver = webdriver.Chrome(options=options)
    
    def get_attractions_page(self):
        """
        Finds the Lonely Planet attractions page for a given location using Selenium.

        Parameters:
            location (str): The location to search for (e.g., 'new york').

        Returns:
            str: The URL of the attractions page if found, or an error message if not.
        """
        

        try:
            search_url = f"https://www.lonelyplanet.com/search?places%5Bquery%5D={self.location.replace(' ', '%20')}"
            self.driver.get(search_url)

            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.CLASS_NAME, "w-full"))
            )

            link = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "a.card-link"))
            )

            if link:
                base_url = link.get_attribute("href")

                attractions_url = f"{base_url}/attractions"
                return attractions_url
            else:
                return "No results found for the location."

        except Exception as e:
            return f"An error occurred: {e}"


    def parse_attractions_page(self, url):
        """
        Parses the attractions page and extracts details of each attraction.

        Parameters:
            url (str): The URL of the attractions page.

        Returns:
            list: A list of dictionaries containing attraction details (image, name, location, external link).
        """

        attractions = []

        try:
            self.driver.get(url)

            WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CSS_SELECTOR, "li.col-span-1"))
            )

            attraction_elements = self.driver.find_elements(By.CSS_SELECTOR, "li.col-span-1")

            for element in attraction_elements[:5]:
                try:

                    image_element = element.find_element(By.CSS_SELECTOR, "img")
                    image_url = image_element.get_attribute("src")

                    name_element = element.find_element(By.CSS_SELECTOR, ".card-link")
                    name = name_element.text.strip()
                    attraction_link = name_element.get_attribute("href")

                    location_element = element.find_element(By.CSS_SELECTOR, ".text-sm.font-semibold.uppercase")
                    location = location_element.text.strip()

                    self.driver.execute_script("window.open('');")
                    self.driver.switch_to.window(driver.window_handles[1])
                    self.driver.get(attraction_link)

                    google_maps_link = None
                    external_link = None

                    try:
                        inline_links = self.driver.find_elements(By.CSS_SELECTOR, "a.inline-link")
                        for link in inline_links:
                            href = link.get_attribute("href")
                            if "google.com/maps" in href:  
                                google_maps_link = href
                            elif validators.url(href):
                                external_link = href

                    except Exception:
                        google_maps_link = "No Google Maps link found"
                        external_link = "No external link found"

                    self.driver.close()
                    self.driver.switch_to.window(self.driver.window_handles[0])

                    attractions.append({
                        "image": image_url,
                        "name": name,
                        "location": self.location,
                        "google_maps_link": google_maps_link,
                        "external_link": external_link
                    })

                except Exception as e:
                    print(f"Error processing attraction: {e}")
                    continue
        except Exception as e:
            return f"An error occurred: {e}"
        return attractions

    def quit_driver(self):
        self.driver.quit()

    
if __name__ == '__main__':
    l = LonelyPlanetHandler('New York')