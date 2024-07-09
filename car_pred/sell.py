from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.utils import secure_filename
from .models import Car
from . import db
from flask_login import login_required, current_user
import os

sell = Blueprint('sell', __name__)
UPLOAD_FOLDER = 'car_pred/static/uploads/'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@sell.route('/sell', methods=['GET', 'POST'])
@login_required
def sell_car():
    # Check if the user has a seller profile
    if current_user.user_type != 'seller' and not current_user.is_admin:
        flash('Only sellers can list cars for sale.', category='error')
        return redirect(url_for('views.home'))
    
    if request.method == 'POST':
        car_name = request.form.get('car_name')
        company = request.form.get('company')
        year_of_purchase = request.form.get('year_of_purchase')
        price = request.form.get('price')
        kms_driven = request.form.get('kms_driven')
        fuel_type = request.form.get('fuel_type')
        owner_name = request.form.get('owner_name')
        address = request.form.get('address')
        contact_details = request.form.get('contact_details')
        image = request.files['image']

        
        if image.filename == '':
            flash( 'No selected file')
        if image and allowed_file(image.filename):
            filename = secure_filename(image.filename)
            image.save(os.path.join(UPLOAD_FOLDER, filename))
        
            flash('File successfully uploaded')
        else:
            flash('Invalid image format. Allowed formats: png, jpg, jpeg, gif', category='error')
            return redirect(request.url)

        new_car = Car(car_name=car_name, company=company, year_of_purchase=year_of_purchase, price=price,
                      kms_driven=kms_driven, fuel_type=fuel_type, owner_name=owner_name, address=address,
                      contact_details=contact_details, image=filename, user_id=current_user.id)
        db.session.add(new_car)
        db.session.commit()
        flash('Car listed successfully!', category='success')
        return redirect(url_for('views.home'))

    return render_template('sell.html', user=current_user)
