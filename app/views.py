from flask import Blueprint, render_template, request, flash, jsonify, redirect, url_for
from flask_login import login_required, current_user
from bson import ObjectId
from datetime import datetime
from . import mongo

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        destination = request.form.get('destination')
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        group_type = request.form.get('group_type')
        group_size = request.form.get('group_size')
        budget = request.form.get('budget')
        preferences = request.form.getlist('preferences')

        # Validate input (optional)
        if not destination or not start_date or not end_date:
            flash('Please fill out all required fields.', category='error')
            return redirect(url_for('views.home'))

        search_history_entry = {
            "user_id": ObjectId(current_user.id),
            "submission_time": datetime.utcnow(),
            "destination": destination,
            "start_date": datetime.strptime(start_date, "%Y-%m-%d"),
            "end_date": datetime.strptime(end_date, "%Y-%m-%d"),
            "group_type": group_type,
            "group_size": int(group_size),
            "budget": float(budget),
            "preferences": preferences
        }
        mongo.db.search_history.insert_one(search_history_entry)

        flash('Search successfully saved to history!', category='success')
        return redirect(url_for('views.home'))

    return render_template("home.html", user=current_user)


@views.route('/generate', methods=['POST'])
def generate():  

    return jsonify({})

@views.route('/pastitineraries', methods=['GET'])
def past_itineraries():  
    return render_template("saved_itineraries.html", user=current_user)