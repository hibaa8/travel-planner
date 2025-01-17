BASE_PROMPT = """
Your response should:
- Be in valid JSON format.
- Group attractions and restaurants by proximity for each day.
- Each day should include two keys: "attractions" and "restaurants".
- Both "attractions" and "restaurants" should be lists of dictionaries, where each dictionary includes:
- Name: Name of the place.
- Image: URL of the place's image.
- Address: Address of the place.
- Rating: Rating of the place.
- Price Level: Price level of the place (or "N/A" if not available).
- Link: URL link to the place.

Organize the itinerary in the following format:
{
    "itinerary": {
        "Day 1": {
            "attractions": [
                {
                    "name": "Example Attraction",
                    "image": "https://example.com/image.jpg",
                    "address": "123 Example St",
                    "rating": 4.5,
                    "price_level": "Moderate",
                    "link": "https://example.com"
                },
                ...
            ],
            "restaurants": [
                {
                    "name": "Example Restaurant",
                    "image": "https://example.com/image.jpg",
                    "address": "456 Example Ave",
                    "rating": 4.2,
                    "price_level": "High",
                    "link": "https://restaurant.com"
                },
                ...
            ]
        },
        ...
    }
}

Rules:
- Create an plan for each day of their vacation.
- Ensure that attractions and restaurants grouped for each day are close to one another.
- Allocate an appropriate number of attractions and restaurants for each day, depending on the duration of the stay.
- Attractions should be placed before restaurants each day.
- take into account their group, budget, and preferences when selecting the attractions and restaurants.
- Do not include markdown or explanations in your response.
- They keys for each dictionary in your json should be lowercase, as shown in the example.
"""