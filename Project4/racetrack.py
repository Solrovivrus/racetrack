import os
import numpy as np
import pandas as pd
import random
''' Contributors: Derek Logan
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
        
        folderPath = os.path.join("/Users/bigd/Desktop/MSU/CSCI 446/Project4", folder)

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
    def nearestPoint(position):
        pass

# --------------------------------------------------------------------------------------------
    # The didYouCrash() method checks to see if the point the car moved to is in fact a wall.
    # If it is in the wall list, True will be returned, if not, False will be returned
    @staticmethod
    def didYouCrash(wallList, position):
        if position in wallList:
            return True
        else:
            return False


    
