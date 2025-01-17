from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from bson import ObjectId
from datetime import datetime
from .utils.google_places_api import GooglePlacesAPIHandler
from .utils.lonely_planet_handler import LonelyPlanetHandler
from .utils.LLM_handler import LLMHandler
import json
views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        destination = request.form.get('destination')
        start_date = datetime.strptime(request.form.get('start_date'), "%Y-%m-%d")
        end_date = datetime.strptime( request.form.get('end_date'), "%Y-%m-%d")
        group_type = request.form.get('group_type')
        budget = int(request.form.get('budget'))
        preferences = request.form.getlist('preferences')

        if not destination or not start_date or not end_date:
            flash('Please fill out all required fields.', category='error')
            return redirect(url_for('views.home'))

        # Save search history
        search_history_entry = {
            "user_id": ObjectId(current_user.id),
            "submission_time": datetime.utcnow(),
            "destination": destination,
            "start_date": start_date,
            "end_date": end_date,
            "duration": (end_date - start_date).days,
            "group_type": group_type,
            "budget": budget,
            "preferences": preferences
        }
        views.search_hist_collection.insert_one(search_history_entry)
        
        google_api_handler = GooglePlacesAPIHandler(destination, budget)
        lonely_planet_handler = LonelyPlanetHandler(destination)

        restaurants = google_api_handler.get_restaurants()
        attractions = google_api_handler.get_attractions()
        
        popular_attractions = lonely_planet_handler.get_popular_attractions()
        llm_handler = LLMHandler(search_history_entry, attractions, restaurants)

        itinerary = llm_handler.create_itinerary()

        flash('Itinerary successfully created!', category='success')

        return render_template(
            "itinerary.html",
            destination=destination,
            user=current_user,
            itinerary=itinerary,
            popular_attractions=popular_attractions,
            save_option=True
        )

    return render_template("home.html", user=current_user)


@views.route('/save_itinerary', methods=['POST'])
def save_itinerary():
    """
    Save itinerary and popular attractions to the database.
    """
    data = request.json 
    itinerary = data.get('itinerary')
    popular_attractions = data.get('popular_attractions')
    destination = data.get('destination')

    if not itinerary or not popular_attractions:
        return jsonify({'error': 'Itinerary and popular attractions are required'}), 400

    saved_data = {
        "user_id": ObjectId(current_user.id),
        "destination": destination,
        "itinerary": itinerary,
        "popular_attractions": popular_attractions,
        "saved_at": datetime.utcnow(),
    }

    result =  views.iterinaries_collection.insert_one(saved_data)
    return jsonify({'message': 'Itinerary saved successfully', 'id': str(result.inserted_id)}), 201


@views.route('/profile', methods=['GET'])
def get_saved_itineraries():
    """
    Retrieve saved itineraries for the current user.
    """
    user_itineraries =  views.iterinaries_collection.find({"user_id": ObjectId(current_user.id)})
    itineraries = [
        {
            "id": str(itinerary["_id"]),
            "destination": str(itinerary["destination"]),
            "saved_at": itinerary["saved_at"],
            "itinerary_preview": itinerary["itinerary"],
        }
        for itinerary in user_itineraries
    ]
    return render_template('profile.html', itineraries=itineraries, user=current_user)

@views.route('/view_itinerary/<itinerary_id>', methods=['GET'])
def view_itinerary(itinerary_id):
    """
    View a specific itinerary by its ID.
    """
    itinerary =  views.iterinaries_collection.find_one({"_id": ObjectId(itinerary_id)})

    if not itinerary:
        return jsonify({'error': 'Itinerary not found'}), 404

    return render_template(
        'itinerary.html',
        destination = itinerary['destination'],
        user=current_user,
        itinerary=itinerary['itinerary'],
        popular_attractions=itinerary['popular_attractions'],
        save_option=False
    )
