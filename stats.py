from flask import (Blueprint, request, jsonify)
from models import Stats
from app import db

stats_bp = Blueprint("stats", __name__, url_prefix='/stats')


# Initialization of rows in the table stats
if __name__ == '__main__':
    db.session.add_all([
        Stats(-1, 0, 0),
        Stats(0, 0, 0),
        Stats(1, 0, 0),
        Stats(2, 0, 0),
        Stats(3, 0, 0)
    ])

    db.session.commit()
