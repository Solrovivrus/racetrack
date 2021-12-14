import os
import numpy as np
import pandas as pd
import random
''' Contributors: Derek Logan, Alyse Mize
----------------------------------------------------------------------------------------------
racetrack's job is to first read in the racetracks from .txt files in its first method and then
    to format a puzzle when given a matrix as a parameter. This class also contains methods for
    returning a random starting position and finding the nearest track point for the mild crash
    paradigm. 
----------------------------------------------------------------------------------------------
'''
class racetrack:
# --------------------------------------------------------------------------------------------
    # The racetrackBuilder() method reads in all racetracks and stores them in np arrays
    @staticmethod
    def racetrackBuilder(folder):
        
        folderPath = os.path.join("C:\\Users\dlogan\Desktop\CSCI446\Project4", folder)

        racetracks = []
        for file in os.listdir(folderPath):
            data = pd.read_csv(os.path.join(folderPath, file), header=None, skiprows = 1)
            f = np.array(data)
            for array in f:
                for i in range(0, len(array)):
                    if array[i] != '.':
                        continue
            racetracks.append(f)
        return racetracks

# --------------------------------------------------------------------------------------------
    # The startFinish() method takes a track and returns the coordinates of the start and finish
    # points in a list. 
    @staticmethod
    def startFinish(track):
        starts = []
        finishes = []
        walls = []
        trackPoints = []
        for i, row in enumerate(track):
            for j, val in enumerate(row):
                if val == 'S':
                    starts.append((i,j))
                elif val == 'F':
                    finishes.append((i,j))
                elif val == '#':
                    walls.append((i,j))
                elif val == '.':
                    trackPoints.append((i,j))

        return(starts, finishes, walls, trackPoints)

# --------------------------------------------------------------------------------------------
    # The starting() method takes the list of possible locations and picks one at random 
    @staticmethod
    def starting(starts):
        start = random.choice(starts)
        return(start)

# --------------------------------------------------------------------------------------------
    # The nearestPoint() method is used in the 'mild' crash paradigm and finds the nearest point
    # on the racetrack for resetting the car on the track. This method takes in the position of 
    # the crash and returns the point to place the car. 
    @staticmethod
    def nearestPoint(position, trackLocations):
        currentPosition = np.array(position)
        trackLocations = np.array(trackLocations)
        distance = np.sum(np.square(trackLocations - currentPosition), axis=1)
        nearest = np.argmin(distance)
        print(nearest)
        print(trackLocations)
        nearestTrack = trackLocations[nearest]

        return nearestTrack

# --------------------------------------------------------------------------------------------
    # The didYouCrash() method checks to see if the point the car moved to is in fact a wall.
    # If it is in the wall list, True will be returned, if not, False will be returned
    @staticmethod
    def didYouCrash(wallList, position):
        if position in wallList:
            return True
        else:
            return False
################## NEED TO THINK ABOUT GOING OFF GAME BOARD

# --------------------------------------------------------------------------------------------
    # The didYouFinish() method checks to see whether or not the point the car has moved to is
    # a finish line space or not
    @staticmethod
    def didYouFinish(finishList, position):
        if position in finishList:
            return True
        else:
            return False
################## NEED TO UPDATE TO INCLUDE IF CAR GOES 'PAST' FINISH LINE NOT JUST LANDS ON IT

# --------------------------------------------------------------------------------------------
    # The updateTrack() class is similar to the vroomvroom class as it also moves the car in the racetrack.
    # However, it is instead used just for the SARSA class as it returns to SARSA the updated track with the new
    # position and updates some key values, such as the reward system.  It checks whether or not the car crashed into a
    # a wall or crossed the finish line and returns bad/good rewards for doing so.  After which it will return the new
    # position to then be graded by the SARSA algorithm training.
    @staticmethod
    def updateTrack(currentPosition, velocity, possAccel, finishes, walls, racetracks):
        reward = 0
        # current position becomes the old position
        oldPosition = currentPosition
        # new position is created based off velocity and old position
        newPosition = [oldPosition[0] + velocity[0], oldPosition[1] + velocity[1]]

        # getting list of positions moved through
        # x coordinates
        if newPosition[0] >= oldPosition[0]:
            xRange = list(range(oldPosition[0], newPosition[0] + 1))
        elif newPosition[0] < oldPosition[0]:
            xRange = list(range(newPosition[0], oldPosition[0] - 1, -1))
        # y coordinates
        if newPosition[1] >= oldPosition[1]:
            yRange = list(range(oldPosition[1], newPosition[1] + 1))
        elif newPosition[1] < oldPosition[1]:
            yRange = list(range(newPosition[1], oldPosition[1] - 1, -1))

        movedThrough = []
        for x, y in zip(xRange, yRange):
            movedThrough.append(list(x, y))

        movedThrough.append(newPosition)

        for position in movedThrough:
            if racetrack.didYouFinish(finishes, position):
                reward = 1
                return True

        for position in movedThrough:
            if racetrack.didYouCrash(walls, position):
                newPosition = racetrack.pickCrashType(currentPosition, movedThrough, racetracks)
                reward = -1

        velocity = racetrack.velocity(possAccel, velocity)

        return newPosition, velocity, currentPosition.didYouFinish, reward
    
   # --------------------------------------------------------------------------------------------
    # This function works with the updateTrack function to test whether it is a soft or hard crash after the car hits a
    # wall.  Depending on the outcome the car either starts at the beginning or starts at the nearest position.
    def pickCrashType(currentPosition, trackLocations, racetracks):
        race = racetrack
        lStarts, lFinishes, lWalls, lPoints = race.startFinish(racetracks)
        crashTypes = ["harshCrash", "softCrash"]
        pickCrash = random.choice(crashTypes)
        if pickCrash == "softCrash":
            currentPosition = race.nearestPoint(currentPosition, trackLocations)
        if pickCrash == "harshCrash":
            currentPosition = race.starting(lStarts)
        return currentPosition


# --------------------------------------------------------------------------------------------
    # The vroomVroom() class actually moves the car in the racetrack. The racetrack takes in the
    # current velocity and determines if the car moved to another track point, crashes, or comes 
    # to the finish line. 
    @staticmethod
    def vroomVroom(currentPosition, velocity, points, finishes, walls, startingPos):
        # current position becomes the old position
        oldPosition = currentPosition
        # new position is created based off velocity and old position
        newPosition = [oldPosition[0] + velocity[0], oldPosition[1] + velocity[1]]

        # getting list of positions moved through
        # x coordinates
        if newPosition[0] >= oldPosition[0]:
            xRange = list(range(oldPosition[0], newPosition[0]+1))
        elif newPosition[0] < oldPosition[0]:
            xRange = list(range(newPosition[0], oldPosition[0]-1, -1))
        # y coordinates
        if newPosition[1] >= oldPosition[1]:
            yRange = list(range(oldPosition[1], newPosition[1]+1))
        elif newPosition[1] < oldPosition[1]:
            yRange = list(range(newPosition[1], oldPosition[1]-1, -1))

        movedThrough = []
        for x,y in zip(xRange, yRange):
            movedThrough.append(list((x,y)))
        
        # returning false and original starting position to reset for mild crash
        for position in movedThrough:
            if racetrack.didYouCrash(walls, position):
                newPosition = startingPos
                return False, newPosition

        movedThrough.append(newPosition)
        print(movedThrough)
        for position in movedThrough:
            if racetrack.didYouFinish(finishes, position):
                return True, newPosition

        return False, newPosition
        

# --------------------------------------------------------------------------------------------
    # The velocity() class updates the vehicles velocity. 
    @staticmethod
    def velocity(acceleration, velocity):
        # easy enough, velocity updates by adding proposed acceleration 
        newX = velocity[0] + acceleration[0]
        newY = velocity[1] + acceleration[1]
        proposed = [newX, newY]

        # also need to check if in limit of -5 to 5
        if abs(newX) <= 5 and abs(newY) <= 5:
            velocity = proposed
            return velocity
        else:
            return velocity



        
    
            

        


