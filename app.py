from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

from persistence.db_config import init_db, get_session
from controller import auth_controller, courier_controller, location_controller
from service.auth_service import register

app = Flask(__name__)
app.url_map.strict_slashes = False

CORS(app)

init_db()

app.register_blueprint(auth_controller.auth_bp)
app.register_blueprint(courier_controller.courier_bp)
app.register_blueprint(location_controller.location_bp)

try:
    register(get_session(), {
        "name": "Mario",
        "surname": "Rossi",
        "email": "mariorossi@example.com",
        "password": "ciao123"
    })
except Exception as x:
    print("Couldn't create admin account:", x)

if __name__ == "__main__":
    app.run(debug=True, port=5001)