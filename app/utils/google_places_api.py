import requests
import os
from dotenv import load_dotenv
load_dotenv()

class GooglePlacesAPIHandler:
    def __init__(self, city, min_price, max_price):
        API_KEY = os.getenv("GOOGLE_PLACES_KEY")
  
        self.city = city
        self.query = f"restaurants in {self.city}"
        self.min_price = min_price  # Budget level: 0 (free) to 4 (very expensive)
        self.max_price = max_price  

        self.min_rating = 4.0 
        self.max_results = 10  
        self.url = "https://maps.googleapis.com/maps/api/place/textsearch/json"

        self.params = {
            "query": self.query,
            "minprice": min_price,
            "maxprice": max_price,
            "key": API_KEY
        }

    def get_restraunts(self):

        places = []
        response = requests.get(self.url, params=self.params)

        if response.status_code == 200:
            data = response.json()
            results = data.get("results", [])
            
            for place in results:
                place_data = {
                    "name": place.get("name"),
                    "address": place.get("formatted_address"),
                    "image": None,  
                    "rating": place.get("rating"),
                    "price_level": place.get("price_level"),
                    "coordinates": place.get("geometry", {}).get("location"),
                    "types": place.get("types", []),
                }

                photos = place.get("photos", [])
                if photos:
                    place_data["image"] = (
                        f"https://maps.googleapis.com/maps/api/place/photo"
                        f"?maxwidth=400&photoreference={photos[0].get('photo_reference')}&key={self.api_key}"
                    )

                places.append(place_data)

                if len(places) >= self.max_results:
                    break

        else:
            print(f"Error: {response.status_code}, {response.text}")

