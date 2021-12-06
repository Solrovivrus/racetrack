import os
import numpy as np
import pandas as pd
import string
''' Contributors: Derek Logan
----------------------------------------------------------------------------------------------
racetrack's job is to first read in the racetracks from .txt files in its first method and then
    to format a puzzle when given a matrix as a parameter. 
----------------------------------------------------------------------------------------------
'''

class racetrack:
    
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

    @staticmethod
    def startFinish(track):
        starts = []
        finishes = []
        for i, row in enumerate(track):
            for j, val in enumerate(row):
                if val == 'S':
                    starts.append((i,j))
                elif val == 'F':
                    finishes.append((i,j))
        
        return(starts, finishes)
