from flask import (Blueprint, request)

bp = Blueprint('move', __name__, url_prefix='/move')


@bp.route('/', methods=['POST', 'GET'])
def get_move():
    if request.method == 'GET':
        return "Test funziona!"
    
