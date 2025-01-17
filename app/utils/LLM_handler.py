import google.generativeai as genai

from dotenv import load_dotenv
import os
import json
from constants import BASE_PROMPT

load_dotenv()

class LLMHandler:
    def __init__(self, form_data, attractions, restaurants):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        self.form_data = form_data
        self.attractions = attractions
        self.restraunts = restaurants

    def create_itinerary(self):
        """
        Generates an itinerary using LLM based on attractions, restaurants, user preferences, and stay duration.
        
        Returns:
            dict: Parsed JSON itinerary.
        """
        destination = self.form_data['destination']
        duration = int(self.form_data['duration'])
        budget = self.form_data['budget']
        preferences = self.form_data['preferences']
        group_type = self.form_data['group_type']

        attractions_description = "\n".join(
            [
                f"- Name: {attraction['name']}\n"
                f"  Address: {attraction['address']}\n"
                f"  Image: {attraction['image']}\n"
                f"  Rating: {attraction['rating']}\n"
                f"  Price Level: {attraction.get('price_level', 'N/A')}\n"
                f"  Link: {attraction['website']}\n"
                for attraction in self.attractions
            ]
        )

        restaurants_description = "\n".join(
            [
                f"- Name: {restaurant['name']}\n"
                f"  Address: {restaurant['address']}\n"
                f"  Image: {restaurant['image']}\n"
                f"  Rating: {restaurant['rating']}\n"
                f"  Price Level: {restaurant.get('price_level', 'N/A')}\n"
                f"  Link: {restaurant['website']}\n"
                for restaurant in self.restraunts
            ]
        )

        unique_section_prompt = f"""
        You are an expert JSON generator for travel itineraries. Based on the following information, create a {duration}-day itinerary for the user that best suits their needs and company:
        - Location: {destination}
        - Budget: {budget}
        - Preferences: {', '.join(preferences)}
        - Group type: {group_type}

        Here is a list of attractions:
        {attractions_description}

        Here is a list of restaurants:
        {restaurants_description}
        \n
        """
        base_prompt = BASE_PROMPT

        prompt = unique_section_prompt + base_prompt

        genai.configure(api_key=os.getenv("GEMINI_KEY"))
        model = genai.GenerativeModel("gemini-1.5-flash")
        try:

            response = model.generate_content(prompt).text.strip()
            response = response.replace("```json", "").replace("```", "").strip()

            itinerary = json.loads(response)
            print("Generated Itinerary:", json.dumps(itinerary, indent=4))

            return itinerary
        except json.JSONDecodeError as e:
            print("Error parsing LLM response to JSON:", e)
            print("LLM Response:", response)
            raise ValueError("The LLM did not return valid JSON. Please try again.")
        except Exception as e:
            print("Error calling Gemini API:", e)
            raise ValueError("An error occurred while generating the itinerary.")