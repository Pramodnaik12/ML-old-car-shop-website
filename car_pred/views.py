from flask import Blueprint, render_template, request, redirect, url_for, jsonify,flash, send_from_directory
from flask_login import login_required, current_user
from .models import Car

views = Blueprint('views', __name__)

@views.route('/')
@login_required
def home():
    return render_template('home.html', user=current_user)

@views.route('/marketplace', methods=['GET'])
def marketplace():
    if current_user.user_type != 'buyer' and not current_user.is_admin:
        flash('Only buyers can access this page.', category='error')
        return redirect(url_for('views.home'))
    cars = Car.query.all()
    return render_template('marketplace.html',  cars=cars, user=current_user)

@views.route('/uploads/<filename>')
def display_image(filename):
    return send_from_directory('static/uploads', filename)





