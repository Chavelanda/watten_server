from flask import (Blueprint, request)


bp = Blueprint('move', __name__, url_prefix='/move')


@bp.route('/getMove', methods=['POST'])
def get_move():
    return 'Todo...'


