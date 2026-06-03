from flask import Flask
from flask_cors import CORS

from persistence.db_config import init_db, get_session
from sqlalchemy import select

from model.delivery_state import DeliveryState
from model.next_delivery_state import NextState

app = Flask(__name__)

CORS(app)

init_db()

session = get_session()

ordered_state = session.get(DeliveryState, 0)
print(ordered_state.next_states)
print(ordered_state.next_states[0].next_state.next_states)

if __name__ == "__main__":
    app.run(debug=True, port=5001)