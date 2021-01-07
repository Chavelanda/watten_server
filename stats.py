from flask import (Blueprint, request, jsonify)
from app import db

stats_bp = Blueprint("stats", __name__, url_prefix='/stats')

from models import Stats


@stats_bp.route('/get/<gen_>')
def get_stats(gen_):

    if -1 <= int(gen_) < 4:
        try:
            stat = Stats.query.filter_by(generation=gen_).first()
            return jsonify(stat.serialize())
        except Exception as e:
            return str(e)

    return jsonify({'error': 'The generation does not exists'}), 400



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
