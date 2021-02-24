from flask import (Blueprint, request, jsonify)
import numpy as np

from watten.games.HandWattenGame import HandWattenGame
from watten.models.HandWattenNNet import HandWattenNNet
from watten.models.DefaultFFNN import DefaultFFNN
from watten.models.CNN import CNN

bp = Blueprint('move', __name__, url_prefix='/move')

cnn_model = "watten/models/cnn_199.h5"

ffnn_model = "watten/models/ffnn_199.h5"

games = [HandWattenGame(), HandWattenGame(cnn=True)]

x, y = games[0].get_observation_size()

x1, y1, z1 = games[1].get_observation_size()

models = [DefaultFFNN(x, y, 1, games[0].get_action_size(), ffnn_model),
          CNN(x1, y1, z1, games[1].get_action_size(), cnn_model)]


@bp.route('/', methods=['POST', 'GET'])
def get_move():
    if request.method == 'GET':
        return "Test funziona!"
    if request.method == 'POST':
        # Take data from json
        json = request.json

        gen = json["generation"]

        games[gen].trueboard.init_world_to_state(-1, json["distributing"], json["hand_a"], json["hand_b"],
                                                 json["played_cards"], json["current_score_a"], json["current_score_b"],
                                                 json["current_prize"], json["is_last_move_raise"],
                                                 json["is_last_move_accepted_raise"], json["is_last_hand_raise_valid"],
                                                 json["first_card"], json["last_card"], json["rank"], json["suit"])

        # Ask to the indicated model to make a prediction
        pi, _ = models[gen].predict(games[gen], games[gen].get_cur_player())

        # Filter the prediction with the valid actions
        valid_moves = games[gen].get_valid_moves(games[gen].get_cur_player())

        pi = pi*valid_moves

        # Return the best possible action
        move = np.argmax(pi)

        answer = {"move": int(move)}

        return jsonify(answer)
