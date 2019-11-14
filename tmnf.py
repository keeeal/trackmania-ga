#!/usr/bin/env python
#coding=utf-8

import time, random, os, io, pickle, functools, keyboard

class Controller(object):
    """Control interface for TrackMania Nations Forever"""
    def __init__(self, autosave_file, speed_file, stats_file):
        self.autosave = autosave_file
        self.pickle = speed_file
        self.stats = stats_file

    def delete_autosave(self):
        if os.path.isfile(self.autosave):
            os.remove(self.autosave)

    def get_score(self):
        with io.open(self.autosave, 'r', encoding='utf-8', errors='ignore') as f:
            return int(f.read().split("times best=\"", 1)[1].split("\"", 1)[0])

    def get_speed(self):
        try:
            f = open(self.pickle)
            return pickle.load(f)
        except:
            return None

    def set_best(self, new_best):
        if new_best:
            f = open(self.stats, 'w')
            pickle.dump(new_best, f)
            f.flush()
            f.close()
        else:
            self.set_best(Race(self, 0, 0))

    def get_best(self):
        try:
            f = open(self.stats)
            return pickle.load(f)
        except:
            return None

    def reset(self):
        keyboard.press_and_release('return')
        time.sleep(1)
        self.delete_autosave()
        time.sleep(1)
        self.delete_autosave()
        time.sleep(1)
        keyboard.press_and_release('return')
        time.sleep(1)
        self.delete_autosave()
        time.sleep(1)
        self.delete_autosave()
        time.sleep(1)
        keyboard.press_and_release('return')

@functools.total_ordering
class Race(object):
    """Race sequence individual"""
    def __init__(self, game, gen, ind, L=None, R=None, n_base=150, p_turn=0.25):
        self.game = game
        self.gen = gen
        self.ind = ind
        self.time = 0
        self.finish = False
        self.maxspeed = 0
        self.distance = 0
        self.L, self.R = [], []

        if L and R:
            self.L, self.R = L, R
        else:
            self.L = [random.random() < p_turn for i in range(n_base)]
            self.R = [random.random() < p_turn for i in range(n_base)]

    def __eq__(self, other):
        if isinstance(other, Race):
            return self.finish == other.finish and self.time == other.time
        else:
            return NotImplemented

    def __lt__(self, other):
        if isinstance(other, Race):
            if self.finish != other.finish:
                return self.finish > other.finish
            if self.finish:
                return self.time < other.time
            else:
                return self.maxspeed > other.maxspeed
        else:
            return NotImplemented

    def __hash__(self):
        return id(self)

    def __str__(self):
        return str(self.time)[:-3] + '.' + str(self.time)[-3:] + ' s'

    def evaluate(self):
        self.game.reset()
        time.sleep(2)
        keyboard.press('up')
        time.sleep(1)

        self.finish = False
        stucktime = 0
        for l,r in zip(self.L, self.R):
            keyboard.press('left') if l and not r else keyboard.release('left')
            keyboard.press('right') if r and not l else keyboard.release('right')
            speed = self.game.get_speed()
            time.sleep(0.2)

            # check if finsihed
            if os.path.isfile(self.game.autosave):
                self.finish = True
                break

            # check if stuck
            if speed < 5:
                stucktime += 1
            else:
                stucktime = 0
            if stucktime > 15:
                break

            # update max speed
            if speed > self.maxspeed:
                self.maxspeed = speed

        keyboard.release('up, down, left, right')

        if self.finish:
            self.time = self.game.get_score()
            self.game.delete_autosave()
            print(self)
            time.sleep(3)
        else:
            self.time = 0
            print('DNF')

        return self.finish
