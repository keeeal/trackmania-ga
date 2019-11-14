#!/usr/bin/env python
#coding=utf-8

import sys, time, random, tmnf

AUTOSAVE_FILE = '/home/j/Documents/TmForever/Tracks/Replays/Autosaves/j_GA.Replay.gbx'
SPEED_FILE = '/home/j/PlayOnLinux\'s virtual drives/TMNations/drive_c/Python27/speedpickle'
STATS_FILE = 'statspickle'

def main():
    n_pop  = 20     # number of individuals
    n_base = 150    # number of key inputs
    k      = 10     # selection pressure
    p_mut  = 0.05   # probability of mutation

    # create game object
    game = tmnf.Controller(AUTOSAVE_FILE, SPEED_FILE, STATS_FILE)
    game.set_best(None)
    time.sleep(5)

    # generate parent population
    gen = 1
    population = [tmnf.Race(game, gen, i+1, n_base=n_base) for i in range(n_pop)]

    # main loop
    while True:
        print('')
        print('GENERATION ' + str(gen))

        # evaluate all individuals
        n_race = 0
        best = game.get_best()
        for p in population:
            n_race += 1
            sys.stdout.write('  Race ' + str(n_race).rjust(3) + ' of ' + str(n_pop) + ':    ')
            sys.stdout.flush()
            finish = p.evaluate()
            if p < best:
                best = p
                game.set_best(p)

        # create new population
        gen += 1
        children = []
        while len(children) < n_pop:

            # choose parents via tournament selection
            p1 = min([random.choice(population) for i in range(k)])
            p2 = min([random.choice(population) for i in range(k)])

            # choose crossover point
            C = random.randrange(1, n_base)

            # mutate child 1
            l = [i != (random.random() < p_mut) for i in p1.L[:C] + p2.L[C:]]
            r = [i != (random.random() < p_mut) for i in p1.R[:C] + p2.R[C:]]
            children.append(tmnf.Race(game, gen, len(children)+1, L=l, R=r))

            # mutate child 2
            l = [i != (random.random() < p_mut) for i in p2.L[:C] + p1.L[C:]]
            r = [i != (random.random() < p_mut) for i in p2.R[:C] + p1.R[C:]]
            children.append(tmnf.Race(game, gen, len(children)+1, L=l, R=r))

        population = children

if __name__ == '__main__':
    main()
