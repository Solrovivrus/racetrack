from racetrack import racetrack
import numpy as np
import string

race = racetrack

tracks = race.racetrackBuilder('tracks')

l = tracks[0]


lStarts, lFinishes = race.startFinish(l)

print(lStarts)


