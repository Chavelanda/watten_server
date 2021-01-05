from flask import (Blueprint, request, jsonify)
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
    if request.method == 'POST':
        # Take data from json
        json = request.json

        gen = json["generation"]

        game.trueboard.init_world_to_state(-1, json["distributing"], json["hand_a"], json["hand_b"],
                                           json["played_cards"], json["current_score_a"], json["current_score_b"],
                                           json["current_prize"], json["is_last_move_raise"],
                                           json["is_last_move_accepted_raise"], json["is_last_hand_raise_valid"],
                                           json["first_card"], json["last_card"], json["rank"], json["suit"])

        # Ask to the indicated model to make a prediction
        pi, _ = models[gen].predict(game, game.get_cur_player())

        # Filter the prediction with the valid actions
        valid_moves = game.get_valid_moves(game.get_cur_player())

        pi = pi*valid_moves

        # Return the best possible action
        move = np.argmax(pi)

        answer = {"move": int(move)}
        
        return jsonify(answer)
