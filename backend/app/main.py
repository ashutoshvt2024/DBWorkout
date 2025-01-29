import logging
from flask import Flask
from flask_cors import CORS
from app.db.session import Base, engine
from app.routes.users import user_blueprint
from app.routes.courses import course_blueprint
from app.routes.tasks import tasks_blueprint
from app.routes.assignments import assignment_blueprint
from app.routes.submissions import submissions_blueprint
from app.routes.schemas import schemas_blueprint
from app.routes.sessions import session_blueprint
from app.routes.auth import auth_blueprint
from flask_jwt_extended import JWTManager
from app.core.config import Config
from logging.handlers import RotatingFileHandler
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# JWT Setup
app.config["JWT_SECRET_KEY"] = Config.SECRET_KEY
jwt = JWTManager(app)
# Set Flask logger to debug mode
app.logger.setLevel(logging.DEBUG)

# Home route
@app.route("/")
def home():
    return "Welcome to the Flask API!"

# Register Blueprints
app.register_blueprint(user_blueprint)
app.register_blueprint(course_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(submissions_blueprint)
app.register_blueprint(schemas_blueprint)
app.register_blueprint(session_blueprint)
app.register_blueprint(assignment_blueprint)
app.register_blueprint(auth_blueprint)

# Initialize database and run server
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        Base.metadata.create_all(bind=engine)
        logging.info("Database initialized successfully")
        app.run(debug=True)
    except Exception as e:
        logging.error(f"Error initializing application: {str(e)}")

# Configure logging
handler = RotatingFileHandler('app.log', maxBytes=100000, backupCount=3)
handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

logging.getLogger().setLevel(logging.INFO)
logging.getLogger().addHandler(handler)