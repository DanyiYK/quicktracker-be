from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()

from persistence.db_config import init_db, get_session
from controller import auth_controller

app = Flask(__name__)

CORS(app)

init_db()

session = get_session()

app.register_blueprint(auth_controller.auth_bp)

if __name__ == "__main__":
    app.run(debug=True, port=5001)