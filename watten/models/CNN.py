import numpy as np
import tensorflow as tf
from keras.models import Model
from keras.layers import Input, Conv2D, MaxPool2D, Flatten, Dense, BatchNormalization, Dropout
from keras.optimizers import Adam
from tensorflow.python.keras.backend import set_session


class CNN:

    def __init__(self, observation_size_x, observation_size_y, observation_size_z, action_size, path_to_model):
        self.observation_size_x = observation_size_x
        self.observation_size_y = observation_size_y
        self.observation_size_z = observation_size_z
        self.action_size = action_size
        self.path_to_model = path_to_model

        self.sess = tf.Session()
        self.graph = tf.get_default_graph()
        set_session(self.sess)
        self.model = self.build_model()
        self.model.load_weights(self.path_to_model)

    def build_model(self):
        print(f"Build model with x {self.observation_size_x}, y {self.observation_size_y}, "
              f"z {self.observation_size_z}, action size {self.action_size}")

        learning_rate = 0.001

        input_boards = Input(shape=(self.observation_size_x, self.observation_size_y, self.observation_size_z))

        print(input_boards.shape)

        cl1 = Conv2D(32, (3, 3), activation='relu')(input_boards)
        cl2 = Conv2D(32, (3, 3), activation='relu')(cl1)
        mp1 = MaxPool2D((2, 2), padding='same')(cl2)
        cl3 = Conv2D(64, (3, 3), activation='relu')(mp1)
        cl4 = Conv2D(64, (3, 3), activation='relu')(cl3)
        mp2 = MaxPool2D((2, 2), padding='same')(cl4)
        f1 = Flatten()(mp2)
        d1 = Dense(128, activation='relu')(f1)
        b1 = BatchNormalization()(d1)
        d1 = Dropout(0.5)(b1)

        pi = Dense(self.action_size, activation='softmax', name='pi')(d1)
        v = Dense(1, activation='tanh', name='v')(d1)

        model = Model(inputs=input_boards, outputs=[pi, v])

        model.summary()

        model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(learning_rate))

        return model

    def predict(self, game, game_player):
        observation = game.get_observation(game_player)
        observation = observation[np.newaxis, :, :, :]

        with self.graph.as_default():
            set_session(self.sess)
            return self.model.predict(observation)

    def clone(self):
        return CNN(self.observation_size_x, self.observation_size_y, self.observation_size_z, self.action_size, self.path_to_model)
