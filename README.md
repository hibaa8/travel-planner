# Travel Planner App

## Overview
The Travel Planner App is a web application designed to simplify trip planning for users. It allows users to generate itineraries based on their preferences and save them for future reference. The app integrates various APIs to provide up-to-date information on attractions, restaurants, and other points of interest.
This planner considers the user's budget constraints, the number of people in their group, and their interests when generating the itinerary.
It then displays a day-by-day itinerary of attractions and restaurants that are grouped based on location proximity. 

## Features
- **Itinerary Generation**: Automatically generates a personalized itinerary based on user input, including attractions and restaurants.
- **Save Itineraries**: Users can save generated itineraries and view them later on their profile.
- **View Saved Itineraries**: Displays saved itineraries as cards that redirect users to a detailed view when clicked.

## Technologies Used
- **Frontend**: HTML, Jinja, CSS, JavaScript
- **Backend**: Flask
- **Database**: MongoDB
- **Web Scraping**: Selenium on Lonely Planet website
- **APIs**: Google Places API and Google Places Detail API


## Setup Instructions
1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo-url/travel-planner.git
   cd travel-planner
   ```

2. Create and activate a virtual environment:
   ```bash
   python3 -m venv myenv
   source myenv/bin/activate  # On Windows: myenv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   
4. Set up API keys for Google Places API and Gemini API and add them to the .env file.

5. Run the Flask application:
   ```bash
   python3 run.py
   ```
   
6. Access the app at [http://127.0.0.1:5000](http://127.0.0.1:5000).


## Next Steps
- **Incorporate Hotel and Flight APIs**: Integrate APIs to fetch the latest hotel booking and flight data based on the user's trip dates and destination.
- **Display Miscellaneous Information**:
  - Weather forecast during the user's stay.
  - Currency exchange rates for international trips.


