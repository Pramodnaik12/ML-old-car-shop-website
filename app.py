from car_pred import create_app
from flask_migrate import Migrate
from car_pred import db
app=create_app()
migrate = Migrate(app, db)  # Initialize Flask-Migrate


if __name__=='__main__':
	app.run(debug=True)