from flask import Flask
from flask_migrate import Migrate
from models import db
from routes import register_routes
import os

app = Flask(__name__)

# Configure secret key for sessions
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with app
db.init_app(app)

# Initialize Flask-Migrate
migrate = Migrate(app, db)

# Register routes
register_routes(app)


if __name__ == '__main__':
    # Create tables
    with app.app_context():
        db.create_all()

    # Run the app
    app.run(debug=True)
