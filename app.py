from flask import Flask
from flask_cors import CORS

from persistence.db_config import init_db, get_session
from sqlalchemy import select

from model.region import Region
from model.province import Province

app = Flask(__name__)

CORS(app)

init_db()

if __name__ == "__main__":
    app.run(debug=True, port=5001)