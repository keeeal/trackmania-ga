#!/usr/bin/env python
#coding=utf-8

import time, tmnf

AUTOSAVE_FILE = '/home/j/Documents/TmForever/Tracks/Replays/Autosaves/j_GA.Replay.gbx'
SPEED_FILE = '/home/j/PlayOnLinux\'s virtual drives/TMNations/drive_c/Python27/speedpickle'
STATS_FILE = 'statspickle'

def main():
    # create game object
    game = tmnf.Controller(AUTOSAVE_FILE, SPEED_FILE, STATS_FILE)
    game.set_best(None)
    time.sleep(5)

    while True:
        for i in range(8):
            print('')
        best = game.get_best()
        print('CURRENT BEST:')
        print('  GEN:    ' + str(best.gen))
        print('  RACE:   ' + str(best.ind))
        print('  TIME:   ' + str(best))
        print('  MAXSPD: ' + str(best.maxspeed))
        print('')
        print('CURRENT SPEED: ' + str(game.get_speed()))
        time.sleep(0.2)

if __name__ == '__main__':
    main()
