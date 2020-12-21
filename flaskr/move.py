from flask import (Blueprint, request, jsonify)
import numpy as np

from flaskr.watten.games.sub_watten.SubWattenGame import WattenSubGame
from flaskr.watten.games.total_watten.TotalWattenGame import TotalWattenGame
from flaskr.watten.nnets.SubWattenNNet import SubWattenNNet
from flaskr.watten.nnets.TotalWattenNNet import TotalWattenNNet

bp = Blueprint('move', __name__, url_prefix='/move')

generations_total = ["flaskr/watten/models/total/gen4.h5", "flaskr/watten/models/total/gen4.h5",
                     "flaskr/watten/models/total/gen4.h5", "flaskr/watten/models/total/gen4.h5"]
generations_sub = ["flaskr/watten/models/sub/model_updated_54.h5", "flaskr/watten/models/sub/model_updated_78.h5",
                   "flaskr/watten/models/sub/model_updated_152.h5", "flaskr/watten/models/sub/best.h5"]


total_nnet = []
sub_nnet = []

# Create sub_game
sub_game = WattenSubGame()

sx, sy = sub_game.get_observation_size()

for i in range(len(generations_sub)):
    sub_nnet.append(SubWattenNNet(sx, sy, 1, sub_game.get_action_size(), generations_sub[i]))

# Create total_watten game
game = TotalWattenGame(sub_nnet[0], sub_nnet[0])

tx, ty = game.get_observation_size()

for i in range(len(generations_total)):
    total_nnet.append(TotalWattenNNet(tx, ty, 1, game.get_action_size(), generations_total[i]))


@bp.route('/', methods=['POST', 'GET'])
def get_move():
    if request.method == 'GET':
        return "Test funziona!"
    elif request.method == 'POST':
        json = request.json

        gen = json["generation"]
        game.sub_watten_agent_player_A = sub_nnet[gen]
        game.sub_watten_agent_player_B = sub_nnet[gen]

        game.trueboard.init_world_to_state(-1, json["distributing"], json["score_a"], json["score_b"], json["hand_a"],
                                           json["hand_b"], json["played_cards"], json["current_score_a"],
                                           json["current_score_b"], json["current_prize"], json["is_last_move_raise"],
                                           json["is_last_move_accepted_raise"], json["is_last_hand_raise_valid"],
                                           json["first_card"], json["last_card"], json["rank"], json["suit"])

        pi, v = total_nnet[gen].predict(game, game.get_cur_player())

        valid_moves = game.get_valid_moves(game.get_cur_player())
        pi = pi*valid_moves

        move = np.argmax(pi)
        if move == 0:
            sub_game.trueboard.init_world_to_state(-1, json["distributing"], json["hand_a"],
                                                   json["hand_b"], json["played_cards"], json["current_score_a"],
                                                   json["current_score_b"], json["first_card"], json["last_card"],
                                                   json["rank"], json["suit"])
            s_pi, v = sub_nnet[gen].predict(sub_game, sub_game.get_cur_player())
            valid_moves = sub_game.get_valid_moves(sub_game.get_cur_player())
            s_pi = s_pi*valid_moves

            sub_move = np.argmax(s_pi)
            d = {"move": int(sub_move)}
        else:
            d = {"move": int(move+45)}

        return jsonify(d)
