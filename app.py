from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

from persistence.db_config import init_db, get_session
from controller import auth_controller
from service.auth_service import register

app = Flask(__name__)

CORS(app)

init_db()

session = get_session()

app.register_blueprint(auth_controller.auth_bp)

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