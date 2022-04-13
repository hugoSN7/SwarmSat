from SwarmNetwork import *
from Trainer import *
import time

swarm = SwarmNetwork(3, 0)

def train(episodes, trainer, swarm):
    for e in range(episodes):
        state = swarm.reset()
        done = False
        steps = 0  # steps in current game
        while not done:
            steps += 1
            action = trainer.get_best_action(state)
            next_state, reward, done, distance, possible_action, _ = swarm.move(action)
            print("next state {}, action {}, distance {}".format(next_state, action, distance))
            trainer.train(state, action, reward, next_state, done)
            #print(state.index(1), Game.ACTION_NAMES[action], reward, next_state.index(1), "DONE" if done else "")
            state = next_state
            if done:
                print("Success")
                break
            if steps > 100:
                trainer.train(state, action, -10, state, True) # we end the game
                break
        if e % 100 == 0: # print log every 100 episode
            print("episode: {}/{}, moves: {}"
                  .format(e, episodes, steps))
            print(f"epsilon : {trainer.epsilon}")
    trainer.save()

trainer = Trainer(learning_rate = 0.01)
train(10, trainer, swarm)
