from flask import (Blueprint, request, jsonify)
import numpy as np

from watten.models.DefaultFFNN import DefaultFFNN

bp = Blueprint('move', __name__, url_prefix='/move')

model_path = "watten/models/model_updated_99.h5"

model = DefaultFFNN(198, 1, 1, 50, model_path)


# c_v ranges from -1 to 1, while the trick played range from 0 to 4
def decide_about_raising(continuous_value, tricks_played, lower_range=0.1, upper_range=0.8):
    # normalize continuous value in range 0 - 1. The make to the power of 5
    norm_cv = ((continuous_value+1) / 2)**5

    # normalize tricks in range 0.2 - 1
    norm_tricks = 0.2 + 0.8*tricks_played/4

    probability = norm_tricks*norm_cv

    # normalize probability in range lower-range - upper-range
    norm_probability = lower_range + (upper_range-lower_range)*probability

    coin = np.random.choice(2, p=[1-norm_probability, norm_probability])

    return coin == 1


# returns true if player should accept raise, false otherwise
def decide_about_accepting_raise(continuous_value, tricks_played):
    return not decide_about_raising(-continuous_value, tricks_played, lower_range=0.02, upper_range=0.8)


@bp.route('/', methods=['POST', 'GET'])
def get_move():
    if request.method == 'GET':
        return "Test funziona!"
    if request.method == 'POST':
        # Take data from json
        json = request.json

        # Composing observation from json
        observation = np.zeros((198,))

        # first card deck
        observation[json["first_card"]] = 1

        # last card deck
        index = 33
        if json["distributing"] == -1:
            observation[index + json["last_card"]] = 1

        # cards in hand
        index += 33  # 66
        player_hand = json["hand_b"]
        for card in player_hand:
            observation[index + card] = 1

        # picked rank
        index += 33  # 99
        rank = json["rank"]
        if rank is not None:
            observation[index + rank] = 1

        # picked suit
        index += 9  # 108
        suit = json["suit"]
        if suit is not None:
            observation[index + suit] = 1

        played_cards = json["played_cards"]
        # last played card
        index += 4  # 112
        if len(played_cards) % 2 == 1:
            observation[index + played_cards[-1]] = 1

        # played cards
        index += 33  # 145
        for card in played_cards:
            observation[index + card] = 1

        # points current hand current player
        index += 33  # 178
        points_current_hand_current = json["current_score_b"]
        if points_current_hand_current != 0:
            observation[index + points_current_hand_current - 1] = 1

        # points current hand opponent player
        index += 2  # 180
        points_current_hand_opponent = json["current_score_a"]
        if points_current_hand_opponent != 0:
            observation[index + points_current_hand_opponent - 1] = 1

        index += 2  # 182
        if json["is_last_move_raise"]:
            observation[index] = 1

        index += 1  # 183
        if json["is_last_move_accepted_raise"]:
            observation[index] = 1

        index += 1  # 184
        if json["is_last_hand_raise_valid"] is None:
            observation[index] = 0
        else:
            observation[index] = 1

        index += 1  # 185
        if json["current_prize"] - 3 >= 0:
            observation[index + json["current_prize"] - 3] = 1

        # total size = 185 + 13 = 198

        observation = observation.reshape((198, 1))
        observation = observation[np.newaxis, :, :]

        pi, v = model.predict(observation)
        pi[46:] = 0

        # transform app valid moves into suitable valid moves for the python game repr
        valid_moves_app = np.array(json["valid_moves"])
        valid_moves = np.zeros((50,))

        valid_moves[:33] = valid_moves_app[:33]
        valid_moves[33:42] = valid_moves_app[33]
        valid_moves[42:46] = valid_moves_app[34]
        valid_moves[46:] = valid_moves_app[35:]

        # Deterministic raising:
        #   - First decide whether to fold
        #   - Then decide whether to raise
        if valid_moves[48] == 1:
            if not decide_about_accepting_raise(v, json["tricks_played"]):
                pi[47] = 1.5

        if valid_moves[46] == 1:
            if decide_about_raising(v, json["tricks_played"]):
                pi[46] = 1.2
            else:
                pi[48] = 1.2

        pi = pi*valid_moves

        if np.sum(pi) == 0:
            pi = valid_moves

        # Return the best possible action
        move = np.argmax(pi)

        answer = {"move": int(move)}

        return jsonify(answer)
