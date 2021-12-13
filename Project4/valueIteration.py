from os import stat
import random
from racetrack import racetrack
import numpy as np
import copy

''' Contributors: Derek Logan
----------------------------------------------------------------------------------------------
valueIterations job is to implement a value iteration model to be used for reinforcement learning.
    This model will train the car/agent to learn how to get from a starting point to the finish
    line as quickly as possible. 
----------------------------------------------------------------------------------------------
'''
# value iteration will need the racetrack, 
class valueIteration:

    @staticmethod
    def valMain(track, points, finishes, walls, position):
        val = valueIteration
        # getting the type of crash to use from the user
        #crash = input('What crash type do you want? 1 = Mild, 100 = HARSH... no in-betweens just pick one:\n')
        # storing acceleration possibilities
        possAccel = [[0,0], [0,-1], [0,1], [-1,0], [-1,-1], [-1,1], [1,0], [1,-1], [1,1]]
        # initializing a starting point to count iterations
        numIterations = 0
        pastValDiff = []
        iterationMax = 100000
        trackDim = np.shape(track)
        trackWidth = trackDim[1]
        trackHeight = trackDim[0]
        print(trackDim[0], trackDim[1], np.shape(track))
        # let's get it going...
        qTable = val.startQTable(trackWidth, trackHeight, possAccel)
        vTable = val.startVTable(trackWidth, trackHeight)
        pTable = val.startVTable(trackWidth, trackHeight)
        print(np.shape(qTable))
        print(np.shape(vTable))

        letsLearn = val.vTrain(vTable, qTable, pTable, pastValDiff, iterationMax, numIterations, possAccel, position, points, finishes, walls, track)
        print("OK..")
        print(letsLearn)
# --------------------------------------------------------------------------------------------
    # The startQTable creates the Q table for value iteration
    @staticmethod
    def startQTable(width, height, possAccel):
        qTable = []
        for w in range(height):
            x = []
            for h in range(width):
                y = []
                for xvel in range(-5,6):
                    xVelocity = []
                    for yvel in range(-5,6):
                        yVelocity = []
                        for a in range(len(possAccel)):
                            yVelocity.append(0)
                        xVelocity.append(yVelocity)
                    y.append(xVelocity)
                x.append(y)
            qTable.append(x)
        return qTable

# --------------------------------------------------------------------------------------------
    # The startVTable creates the value table for value iteration
    @staticmethod
    def startVTable(width, height):
        vTable = []
        for w in range(height):
            x = []
            for h in range(width):
                y = []
                for i in range(11):
                    xVelocity = []
                    for j in range(11):
                        xVelocity.append(0)
                    y.append(xVelocity)
                x.append(y)
            vTable.append(x)
        return vTable
# --------------------------------------------------------------------------------------------
    # The vTrain() method trains our model
    @staticmethod
    def vTrain(vTable, qTable, pTable, pastValDiff, iterationMax, numIterations, possAccel, position, points, finishes, walls, track):
        threshold = .1
        discount = .95
        maxDeltaQ = 9
        startingPos = position
        # we have to keep training until we converge
        haveWeConverged = 0

        while (not haveWeConverged) and (numIterations < iterationMax):
            velocity = [0,0]
            oldValTable = copy.deepcopy(vTable)
            maxDeltaQ = 0

            # updating value table
            for i in range(len(vTable)):
                y = vTable[i]
                for j in range(len(y)):
                    xVelocity = vTable[i][j]
                    for k in range(len(xVelocity)):
                        yVelocity = vTable[i][j][k]
                        for l in range(len(yVelocity)):
                            policy = [0,0]
                            maxQ = -100000

                            for m in range(len(possAccel)):
                                acceleration = possAccel[m]
                                #print("Acceleration: " + str(acceleration))
                                position = [i,j]
                                
                                #updating position after velocity
                                # NEED TO FINISH
                                velocity = racetrack.velocity(acceleration, velocity)
                                #print("Velocity: " + str(velocity))
                                haveYouFinished, position = racetrack.vroomVroom(position, velocity, points, finishes, walls, startingPos)
                                print("Have you finished?", haveYouFinished, position)
                                print(track[position[0]][position[1]])
                                newXVelocity = velocity[0] + 5
                                newYVelocity = velocity[1] + 5
                                newXPosition = position[0]
                                newYPosition = position[1]

                                print(newXPosition, newYPosition, newXVelocity, newYVelocity)
                                numIterations +=1
                                print(numIterations)
                                #values
                                newV = 0
                                reward = -1
                                if haveYouFinished == True:
                                    reward = 0
                                else:
                                    newV = oldValTable[newXPosition][newYPosition][newXVelocity][newYVelocity]

                                newQ = reward + discount*newV
                                qTable[i][j][k][l][m] = newQ

                                if newQ > maxQ:
                                    policy = acceleration
                                    maxQ = newQ
                            
                            oldQ = vTable[i][j][k][l]
                            vTable[i][j][k][l] = maxQ
                            pTable[i][j][k][l] = policy

                            deltaQ = oldQ - maxQ
                            if deltaQ > maxDeltaQ:
                                maxDeltaQ = deltaQ
                            print("Delta: " + str(maxDeltaQ))

                            if maxDeltaQ < threshold:
                                haveWeConverged = True
                            pastValDiff.append(maxDeltaQ)
                            #numIterations += 1

        return pastValDiff

    @staticmethod
    def vTest():
        pass







