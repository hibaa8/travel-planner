import google.generativeai as genai

from dotenv import load_dotenv
import os
load_dotenv()

class LLMHandler:
    def __init__(self):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")


    def create_itinerary(attractions, restaurants, budget, preferences, duration):
        """
        Generates an itinerary using LLM based on attractions, restaurants, user preferences, and stay duration.
        
        Args:
            attractions (list): List of attractions (dictionaries with details).
            restaurants (list): List of restaurants (dictionaries with details).
            budget (str): User's budget ("low", "moderate", "high").
            preferences (list): List of user preferences (e.g., ["cultural", "outdoor"]).
            duration (int): Duration of stay in days.

        Returns:
            str: Generated itinerary.
        """

        attractions_description = "\n".join(
            [
                f"- Name: {attraction['name']}\n"
                f"  Address: {attraction['address']}\n"
                f"  Image: {attraction['image']}\n"
                f"  Rating: {attraction['rating']}\n"
                f"  Price Level: {attraction.get('price_level', 'N/A')}\n"
                f"  Link: https://maps.google.com/?q={attraction['coordinates']['lat']},{attraction['coordinates']['lng']}\n"
                for attraction in attractions
            ]
        )

        restaurants_description = "\n".join(
            [
                f"- Name: {restaurant['name']}\n"
                f"  Address: {restaurant['address']}\n"
                f"  Image: {restaurant['image']}\n"
                f"  Rating: {restaurant['rating']}\n"
                f"  Price Level: {restaurant.get('price_level', 'N/A')}\n"
                f"  Link: https://maps.google.com/?q={restaurant['coordinates']['lat']},{restaurant['coordinates']['lng']}\n"
                for restaurant in restaurants
            ]
        )

        prompt = f"""
        You are an expert HTML generator for travel itineraries. Based on the following information, create a {duration}-day itinerary for the user:
        - Budget: {budget}
        - Preferences: {', '.join(preferences)}

        Here is a list of attractions:
        {attractions_description}

        Here is a list of restaurants:
        {restaurants_description}

        Your response should:
        - Include cards for each attraction and restaurant in the itinerary.
        - Each card should include:
        - The name of the place.
        - Its image (with a URL in an `<img>` tag).
        - Its address.
        - Its rating.
        - Its price level.
        - A clickable link to the place on Google Maps.
        - Organize the itinerary by day, with morning, afternoon, and evening slots.
        - Use a responsive grid layout with up to 3 cards per row.
        - Include CSS for styling: use a flexbox or grid layout for the cards.
        - Format the response as a complete HTML document, ready to be rendered in a browser.
        - Do not include markdown
            """

        genai.configure(api_key=os.getenv("GEMINI_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        try:
            response = model.generate_content(prompt).text
        except Exception as e:
            print(f"Error calling Gemini API: {e}")
        
        return response
