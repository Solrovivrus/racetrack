from racetrack import racetrack
import numpy as np
import string
import random

race = racetrack
tracks = race.racetrackBuilder('tracks')

# starting velocity for all tracks & crash types
startVelocity = [0,0]

# For the L-track
l = tracks[0]
# getting points figured out
lStarts, lFinishes, lWalls, lPoints = race.startFinish(l)
# picking random start point
lStartingPoint = race.starting(lStarts)

print(lStartingPoint)



