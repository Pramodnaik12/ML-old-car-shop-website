# __init__.py
from flask import Flask, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from os import path, makedirs
from flask_login import LoginManager, UserMixin
from flask_admin import Admin
from .admin_view import AdminModelView
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    CORS(app)
    app.config['SECRET_KEY'] = 'JHHGWUDBASHAJD'
    app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_NAME}"
    app.config['UPLOAD_FOLDER'] = 'static/uploads'  # Add upload folder configuration
    db.init_app(app)
    migrate.init_app(app, db)

    admin = Admin(app)
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    from .views import views
    from .auth import auth
    from .pred import pred
    from .sell import sell
      # import the sell blueprint

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(pred, url_prefix='/')
    app.register_blueprint(sell, url_prefix='/')
    
     # register the sell blueprint

    from .models import User, Buyer, Seller, Car
    create_database(app)

    admin.add_view(AdminModelView(User, db.session))
    admin.add_view(AdminModelView(Car, db.session))
    
      # add Car model to admin

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Error handlers
    @app.errorhandler(403)
    def forbidden_error(error):
        return render_template('403.html'), 403

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('404.html'), 404

    return app

def create_database(app):
    if not path.exists('car_pred/' + DB_NAME):
        makedirs('car_pred', exist_ok=True)
        with app.app_context():
            db.create_all()
        print('Created Database!')
