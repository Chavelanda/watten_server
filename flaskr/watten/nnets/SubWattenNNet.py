from keras.models import *
from keras.layers import *
from keras.optimizers import *
from tensorflow.python.keras.backend import set_session
import tensorflow as tf


class SubWattenNNet:

    def __init__(self, obs_x, obs_y, obs_z, act_size, path_to_model):
        self.observation_size_x = obs_x
        self.observation_size_y = obs_y
        self.observation_size_z = obs_z
        self.action_size = act_size
        self.sess = tf.Session()
        self.graph = tf.get_default_graph()
        set_session(self.sess)
        self.model = self.build_model()
        self.path_to_model = path_to_model
        self.model.load_weights(self.path_to_model)

    def build_model(self):
        print(f"Build model with x {self.observation_size_x}, y {self.observation_size_y}, "
              f"z {self.observation_size_z}, action size {self.action_size}")

        learning_rate = 0.0001

        input_boards = Input(shape=(self.observation_size_x, self.observation_size_y))

        x_image = Reshape((self.observation_size_x, self.observation_size_y, 1))(input_boards)

        print(x_image.shape)

        h_input = Flatten()(x_image)

        h_fc1 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(1024)(h_input))))
        h_fc2 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(1024)(h_fc1))))
        h_fc3 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(1024)(h_fc2))))
        h_fc4 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(1024)(h_fc3))))
        h_fc5 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(512)(h_fc4))))
        h_fc6 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(512)(h_fc5))))
        h_fc7 = Dropout(0.2)(Activation('relu')(BatchNormalization(axis=1)(Dense(512)(h_fc6))))

        pi = Dense(self.action_size, activation='softmax', name='pi')(h_fc7)
        v = Dense(1, activation='tanh', name='v')(h_fc7)

        model = Model(inputs=input_boards, outputs=[pi, v])

        model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(learning_rate))

        return model

    def predict(self, game, game_player):
        observation = game.get_observation(game_player)
        observation = observation[np.newaxis, :, :]

        with self.graph.as_default():
            set_session(self.sess)
            return self.model.predict(observation)

    def clone(self):
        return SubWattenNNet(self.observation_size_x, self.observation_size_y, 1, self.action_size, self.path_to_model)
