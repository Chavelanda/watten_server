from flask import (Blueprint, request, jsonify)
from flaskr.db import get_db

bp = Blueprint("stats", __name__, url_prefix='/stats')


@bp.route('/get')
def get_stats():
    generation = int(request.args['gen'])

    if 0 <= generation < 4:
        db = get_db()
        stats = db.execute('SELECT * FROM stats WHERE generation = ?', (generation,)).fetchone()

        if stats is not None:
            response = {'played': stats['played'], 'won': stats['won']}
        else:
            response = {'played': 0, 'won': 0}

        return jsonify(response)

    return jsonify({'error': 'The generation does not exists'}), 400


@bp.route('/insert', methods=['POST'])
def insert_stats():
    json = request.json
    generation = json['generation']
    won = json['won']

    print("Generation " + str(generation))
    print("Won " + str(won))

    db = get_db()

    if 0 <= generation < 4:
        old_stats = db.execute('SELECT * FROM stats WHERE generation = ?', (generation,)).fetchone()
        print(old_stats)
        if old_stats is None:
            db.execute('INSERT INTO stats (generation, played, won) VALUES (?, ?, ?)', (generation, 1, won))
        else:
            db.execute('UPDATE stats SET played = ?, won = ? WHERE generation = ?',
                       (old_stats['played']+1, old_stats['won'] + won, generation))

        db.commit()
        return jsonify({'message': 'Stats updated correctly'}), 200

    return jsonify({'error': 'The generation does not exists'}), 400
