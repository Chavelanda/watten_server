import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense, BatchNormalization, Activation, Dropout, Flatten, Reshape, Input
from tensorflow.keras.models import Model
from tensorflow.keras.optimizers import Adam


class DefaultFFNN:

    def __init__(self, observation_size_x, observation_size_y, observation_size_z, action_size, path_to_model):
        self.observation_size_x = observation_size_x
        self.observation_size_y = observation_size_y
        self.observation_size_z = observation_size_z
        self.action_size = action_size

        devices = tf.config.list_physical_devices('GPU')
        print(devices)

        if len(devices) > 0:
            tf.config.set_soft_device_placement(True)
            tf.debugging.set_log_device_placement(True)

        self.model = self.build_model()
        self.model.load_weights(path_to_model)
        self.graph_model = tf.function(self.model)

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

        model.summary()

        model.compile(loss=['categorical_crossentropy', 'mean_squared_error'], optimizer=Adam(learning_rate))

        return model

    def predict(self, observation):
        pi, v = self.graph_model(observation, training=False)

        if np.isscalar(v[0]):
            return pi[0], v[0]
        else:
            return pi[0], v[0][0]

    def clone(self):
        return DefaultFFNN(self.observation_size_x, self.observation_size_y, 1, self.action_size)
