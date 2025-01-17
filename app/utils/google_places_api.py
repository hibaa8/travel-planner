import requests
import os
from dotenv import load_dotenv

load_dotenv()

class GooglePlacesAPIHandler:
    def __init__(self, city, max_price):
        self.api_key = os.getenv("GOOGLE_PLACES_KEY")
        self.city = city
        self.restaurant_query = f"restaurants in {self.city}"
        self.attraction_query = f"attraction in {self.city}"
        self.max_price = max_price
        self.min_rating = 3.0  
        self.max_results = 15  
        self.places_api_url = "https://maps.googleapis.com/maps/api/place/textsearch/json"
        self.places_details_api_url = "https://maps.googleapis.com/maps/api/place/details/json"

    def get_restaurants(self):
        params = {
            "query": self.restaurant_query,
            "key": self.api_key,
        }
        results = self.call_api(params)
        print(f'restraunts: {results}')
        return results

    def get_attractions(self):
        params = {
            "query": self.attraction_query,
            "key": self.api_key,
        }
        results = self.call_api(params)
        print(f'attractions: {results}')
        return results

    def call_api(self, params):
        places = []
        response = requests.get(self.places_api_url, params=params)

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            filtered_results = [place for place in results if place.get("rating", 0) >= self.min_rating]

            for place in filtered_results:
                if len(places) >= self.max_results:
                    break  

                place_id = place.get("place_id")
                place_name = place.get("name")

                details_params = {
                    "place_id": place_id,
                    "fields": "name,formatted_address,geometry,photos,rating,price_level,website",
                    "key": self.api_key,
                }
                details_response = requests.get(self.places_details_api_url, params=details_params)

                if details_response.status_code != 200:
                    print(f"Error fetching details for {place_name}: {details_response.status_code}")
                    continue

                details_data = details_response.json().get("result", {})

                places.append({
                    "name": details_data.get("name"),
                    "address": details_data.get("formatted_address"),
                    "coordinates": details_data.get("geometry", {}).get("location"),
                    "rating": details_data.get("rating"),
                    "price_level": details_data.get("price_level", "N/A"),
                    "image": (
                        f"https://maps.googleapis.com/maps/api/place/photo?maxwidth=400"
                        f"&photoreference={place.get('photos', [{}])[0].get('photo_reference', '')}&key={self.api_key}"
                        if place.get("photos") else None
                    ),
                    "website": details_data.get("website"),
                })
        else:
            print(f"Error: {response.status_code}, {response.text}")

        return places
