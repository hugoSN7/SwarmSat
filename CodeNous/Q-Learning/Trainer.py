from SwarmNetwork import *
import numpy as np
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation
from tensorflow.keras.optimizers import Adam, SGD
import random
import time
import os

from collections import deque

class Trainer:
    def __init__(self, name=None, learning_rate=0.01, epsilon_decay=0.9999):
        self.state_size = 100
        self.action_size = 100
        self.gamma = 0.9
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = epsilon_decay
        self.learning_rate = learning_rate
        self.name = name

        if name is not None and os.path.isfile("model-" + name):
            model = load_model("model-" + name)
        else:
            model = Sequential()
            model.add(Dense(24, input_shape=(self.state_size,), activation='relu'))
            model.add(Dense(24, activation="relu"))
            model.add(Dense(self.action_size, activation='linear'))
            model.compile(loss='mse', optimizer=SGD(lr=self.learning_rate))

        self.model = model

    def train(self, state, action, reward, next_state, done):
        target = self.model.predict(np.array(state))[0]
        if done:
            target[action] = reward
        else:
            target[action] = reward + self.gamma * np.max(self.model.predict(np.array([next_state])))

        inputs = np.array([state])
        outputs = np.array([target])

        return self.model.fit(inputs, outputs, epochs=1, verbose=0, batch_size=1)

    def get_best_action(self, state, rand=True):

        self.epsilon *= self.epsilon_decay

        if rand and np.random.rand() <= self.epsilon:
            # The agent acts randomly
            return random.randrange(self.action_size)

        # Predict the reward value based on the given state
        act_values = self.model.predict(np.array([state]))

        # Pick the action based on the predicted reward
        action =  np.argmax(act_values[0])
        return action

    def save(self):
        if self.name:
            self.model.save("model-" + self.name, overwrite=True)
        else:
            self.model.save("model-" + str(time.time()))
