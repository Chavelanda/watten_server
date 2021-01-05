from flask import (Blueprint, request)
import numpy as np

from watten.games.HandWattenGame import HandWattenGame
from watten.models.HandWattenNNet import HandWattenNNet

bp = Blueprint('move', __name__, url_prefix='/move')

generations = ["watten/models/model_updated_3.h5", "watten/models/model_updated_4.h5",
               "watten/models/model_updated_6.h5", "watten/models/model_updated_21.h5"]

models = []

game = HandWattenGame()

x, y = game.get_observation_size()

for path in generations:
    models.append(HandWattenNNet(x, y, 1, game.get_action_size(), path))


@bp.route('/', methods=['POST', 'GET'])
def get_move():
    if request.method == 'GET':
        return "Test funziona!"

