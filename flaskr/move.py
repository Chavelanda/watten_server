from flask import (Blueprint, request, jsonify)
import numpy as np

from flaskr.watten.agents.AgentNNet import AgentNNet
from flaskr.watten.games.sub_watten.SubWattenGame import WattenSubGame
from flaskr.watten.games.total_watten.TotalWattenGame import TotalWattenGame
from flaskr.watten.nnets.SubWattenNNet import SubWattenNNet
from flaskr.watten.nnets.TotalWattenNNet import TotalWattenNNet


bp = Blueprint('move', __name__, url_prefix='/move')

generations_total = ["flaskr/watten/models/total/gen4.h5", "flaskr/watten/models/total/gen4.h5",
                     "flaskr/watten/models/total/gen4.h5", "flaskr/watten/models/total/gen4.h5"]
generations_sub = ["flaskr/watten/models/sub/model_updated_54.h5", "flaskr/watten/models/sub/model_updated_78.h5",
                   "flaskr/watten/models/sub/model_updated_152.h5", "flaskr/watten/models/sub/best.h5"]

# Set up environment to handle requests
# Create sub_game
sub_game = WattenSubGame()
x, y = sub_game.get_observation_size()

#Create agent for sub_watten
sub_watten_nnet = SubWattenNNet(x, y, 1, sub_game.get_action_size())

sub_agent_nnet_0 = AgentNNet(sub_watten_nnet)
sub_agent_nnet_1 = sub_agent_nnet_0.clone()
sub_agent_nnet_2 = sub_agent_nnet_0.clone()
sub_agent_nnet_3 = sub_agent_nnet_0.clone()

sub_agent_nnet_0.load(generations_sub[0])
sub_agent_nnet_1.load(generations_sub[1])
sub_agent_nnet_2.load(generations_sub[2])
sub_agent_nnet_3.load(generations_sub[3])

#Create total_watten game
game = TotalWattenGame(sub_agent_nnet_0, sub_agent_nnet_0)

#Create agent for total_watten
x, y = game.get_observation_size()
total_watten_nnet = TotalWattenNNet(x, y, 1, game.get_action_size())

agent_nnet_0 = AgentNNet(total_watten_nnet)
agent_nnet_1 = agent_nnet_0.clone()
agent_nnet_2 = agent_nnet_0.clone()
agent_nnet_3 = agent_nnet_0.clone()

agent_nnet_0.load(generations_total[0])
agent_nnet_1.load(generations_total[1])
agent_nnet_2.load(generations_total[2])
agent_nnet_3.load(generations_total[3])

total_agents = [agent_nnet_0, agent_nnet_1, agent_nnet_2, agent_nnet_3]

sub_agents = [sub_agent_nnet_0, sub_agent_nnet_1, sub_agent_nnet_2, sub_agent_nnet_3]


@bp.route('/', methods=['POST', 'GET'])
def get_move():
    if request.method == 'GET':
        return "Test funziona!"
    elif request.method == 'POST':
        json = request.json

        gen = json["generation"]
        game.sub_watten_agent_player_A = sub_agents[gen]
        game.sub_watten_agent_player_B = sub_agents[gen]

        game.trueboard.init_world_to_state(-1, json["distributing"], json["score_a"], json["score_b"], json["hand_a"],
                                           json["hand_b"], json["played_cards"], json["current_score_a"],
                                           json["current_score_b"], json["current_prize"], json["is_last_move_raise"],
                                           json["is_last_move_accepted_raise"], json["is_last_hand_raise_valid"],
                                           json["first_card"], json["last_card"], json["rank"], json["suit"])

        pi, v = total_agents[gen].predict(game, game.get_cur_player())

        valid_moves = game.get_valid_moves(game.get_cur_player())
        pi = pi*valid_moves

        move = np.argmax(pi)
        print(move)
        if move == 0:
            sub_game.trueboard.init_world_to_state(-1, json["distributing"], json["hand_a"],
                                                   json["hand_b"], json["played_cards"], json["current_score_a"],
                                                   json["current_score_b"], json["first_card"], json["last_card"],
                                                   json["rank"], json["suit"])
            s_pi, v = sub_agents[gen].predict(sub_game, sub_game.get_cur_player())
            valid_moves = sub_game.get_valid_moves(sub_game.get_cur_player())
            s_pi = s_pi*valid_moves

            sub_move = np.argmax(s_pi)
            print(sub_move)
            d = {"move": sub_move}
        else:
            d = {"move": move+45}

        return jsonify(d)


