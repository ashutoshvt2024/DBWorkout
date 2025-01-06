from flask import Flask
from app.db.session import Base, engine
from app.api.users import user_blueprint
from app.api.tasks import tasks_blueprint
from app.api.submissions import submissions_blueprint
from app.api.schemas import schemas_blueprint
from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
@app.route("/")
def home():
    return "Welcome to the Flask API!"

# Register blueprints
app.register_blueprint(user_blueprint)
app.register_blueprint(tasks_blueprint)
app.register_blueprint(submissions_blueprint)
app.register_blueprint(schemas_blueprint)

if __name__ == "__main__":
    Base.metadata.create_all(bind=engine)
    app.run(debug=True)