import os
import numpy as np
import pandas as pd
import random
from racetrack import racetrack

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
    # chooseAction() will pick an action for the race car.  If the car is above the learning rate of epsilon it will
    # then choose actions that are slightly less random as it prioritize more "good" actions over random actions.
    def chooseAction(raceTrack, states, epsilon):

        values = [raceTrack [states, :]]
        maxStates = max(values)
        actions = [action for action in range(len(values))]
        greed = [action for action in range(len(values)) if values[action] == maxStates]

        chooseAction = random.random()
        if chooseAction < epsilon:
            return random.choice(actions)
        else:
            return random.choice(greed)

    # --------------------------------------------------------------------------------------------
    # updateAction() will update the reward system for the track to better decide for the greedy algorithm which
    # algorithms are better/worse and which ones to choose.
    def updateAction(raceTrack, currentState, currentAction, reward, nextAction, nextState, alpha, gamma):
        racetrackCurrent = racetrack[currentState, currentAction]
        raceTrackNext = raceTrack[nextState, nextAction]
        updateReward = (reward + gamma * raceTrackNext) - racetrackCurrent
        racetrackCurrent = racetrackCurrent + alpha * updateReward

    # --------------------------------------------------------------------------------------------
    # get_racetrack() returns an empty array which will set up our reward system for which spots are better/worse.
    # for the finish/starting line those spots are 1and .5 and for walls/track the values are zero.  The idea being that
    # if the car hits a wall the updateTrack function will make that reward spot a -1 to teach the car to not hit that
    # area.  The rest of the track however will be updated with values depending on how good/bad they are.
    def get_racetrack(racetracks):
        racetrack = []
        row = []
        for arr in racetracks:
            racetrack.append(row)
            string = arr[0]
            string = string.replace("#", "0")
            string = string.replace(".", "0")
            string = string.replace("S", ".5")
            string = string.replace("F", "1")
            for c in string:
                row.append(int(c))
            row = []
        return racetrack


    # --------------------------------------------------------------------------------------------
    # The trainCar() function is the main function for SARSA as it connects to all other related functions.  This
    # function sets up all the variables such as epsilon, alpha, and gamma which are the rates of learning for the
    # training function.  It will then go through a number of iterations to train the car into reaching the finish line
    # because the finish line has the highest value of 1 it incentives the car to reach that line as it has the highest
    # value. By iterating and picking random actions that lead to random spots the car will travel around the board
    # until it finds the best route, hypothetically.
    def trainCar(racetracks):
        Sar = SARSA
        race = racetrack
        lStarts, lFinishes, lWalls, lPoints = race.startFinish(racetracks)
        maxRaces = 1000
        maxState = 100
        epsilon = .9
        alpha = .85
        gamma = .95
        crashes = 0
        reward = 0
        velocity = [0, 0]
        track = Sar.get_racetrack(racetracks)
        possAccel = [[0,0], [0,-1], [0,1], [-1,0], [-1,-1], [-1,1], [1,0], [1,-1], [1,1]]
        possAccel = random.choice(possAccel)

        for i in range(maxRaces):
            initialState = track
            initialAction = Sar.chooseAction(track, initialState, epsilon)

            for state in range(maxState):
                nextState, velocity, crossedFinish, reward = race.updateTrack(initialState, velocity, possAccel, lFinishes, lWalls, racetracks)

                nextAction = Sar.chooseAction(track, nextState, epsilon)

                Sar.updateAction(track, initialState, initialAction, reward, nextAction, nextState, alpha, gamma)

                initialState, initialAction = nextState, nextAction

                if crossedFinish:
                    print("You crossed the finish line!")
                    print(track)
                    break
