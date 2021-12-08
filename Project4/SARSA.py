import os
import numpy as np
import pandas as pd
import random
import racetrack
import racetrack

'''Contributors: Alyse Mize 
---------------------------------------------------------------------------------------------- 
SARSA is a reinforcement learning algorithm that is passive.  SARSA starts by initializing the summation of rewards 
after performing action a while in state s (Q(s,a)) for all states and all actions for each state arbitrarily. Following 
this, for each episode the state will be initialized and our agent will choose an action a using a specific policy 
which has been determined from Q(s,a). Once this is done, repeatedly the agent will apply another action a and 
observe the given reward and following state s’. Following taking that action, the agent will choose a new action a 
using the policy derived from Q and then update Q given the past Q. 

----------------------------------------------------------------------------------------------
'''


class SARSA:
    # --------------------------------------------------------------------------------------------
    # chooseAction() will pick an action for the race car

    def chooseAction(raceTrack, states, epsilon):

        values = raceTrack[states, :]
        maxStates = max(values)
        actions = [action for action in range(len(values))]
        greed = [action for action in range(len(values)) if values[action] == maxStates]

        chooseAction = random.random()
        if chooseAction < epsilon:
            return random.choice(actions)
        else:
            return random.choice(greed)

    def updateAction(raceTrack, currentState, currentAction, reward, nextAction, nextState, alpha, gamma):
        racetrackCurrent = racetrack[currentState, currentAction]
        raceTrackNext = raceTrack[nextState, nextAction]
        updateReward = (reward + gamma * raceTrackNext) - racetrackCurrent
        racetrackCurrent = racetrackCurrent + alpha * updateReward

    def trainCar(racetracks):
        Sar = SARSA
        maxRaces = 1000
        maxState = 100
        epsilon = .9
        alpha = .85
        gamma = .95
        victory = 0  # and by "victory" it could mean either crossing the finish line of just not crashing
        crashes = 0
        reward = 0
        racetrack = racetracks

        for race in range(maxRaces):
            initialState = racetrack.reset()
            initialAction = Sar.chooseAction(racetrack, initialState, epsilon)
            victory = 0

            for state in range(maxState):
                nextState, reward, done, info = racetrack.step(initialAction)

                nextAction = Sar.chooseAction(racetrack, nextState, epsilon)

                Sar.updateAction(racetrack, initialState, initialAction, reward, nextAction, nextState, alpha, gamma)

                initialState, initialAction = nextState, nextAction

                if done:
                    break
