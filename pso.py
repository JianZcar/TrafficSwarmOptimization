import sys
import numpy as np
import argparse
from runner import run_sumo


def pso(nparticles, niters, c0, c1, n_intersections, outfile="pso", min_time=5.,
        max_time=30., max_velocity=10., seed=42):
    # ALGORITHM
    # n: number of particles
    # d: size of position + velocity vector
    # optimus/optimal: globally best position/score
    # primes/primals: agent best position/score
    nstates = 4
    nlights = n_intersections
    # np.random.seed(seed)

    # initialize everything uniformly at random
    positions = np.random.uniform(
        min_time, max_time/2, (nparticles, nlights, nstates))
    velocities = np.random.uniform(-max_velocity,
                                   max_velocity,
                                   (nparticles, nlights, nstates))
    primes = np.zeros((nparticles, nlights, nstates))
    primals = [0]*nparticles
    optimus = np.zeros((nparticles, nlights, nstates))
    optimal = 100000  # really high number
    t = 0  # Initialize t for initial logging

    for i in range(nparticles):
        primals[i] = run_sumo(n_intersections, 'summary.xml', positions[i], "pso")
        primes[i] = positions[i]
        if primals[i] < optimal:
            optimal = primals[i]
            optimus = np.tile(positions[i], (nparticles, 1, 1))

    fh = open("output/"+outfile+"_global.csv", "w")
    fh.write("Iteration, Particle, Mean Travel Time\n")

    fh2 = open("output/"+outfile+"_locals.csv", "w")
    fh2.write("Iteration, Local Bests\n")

    fh3 = open("output/"+outfile+"_gposition.csv", "w")
    fh3.write("Iteration, Particle, Positions\n")

    print("%d " % t, file=fh2)
    print(primals, "\n", file=fh2)
    print("%d, %d, %.5f\n" % (t, i, optimal), file=fh)
    print("%d, %d\n" % (t, i), file=fh3)
    for row in optimus[0]:
        print(row, file=fh3)

    for t in range(niters):
        r0 = np.repeat(np.repeat(
            c0*np.random.random_sample((nparticles, 1, 1)),
                       # , nlights, nstates))
                       nlights, axis=1), nstates, axis=2)
        r1 = np.repeat(np.repeat(
            c1*np.random.random_sample((nparticles, 1, 1)),
                       # , nlights, nstates))
                       nlights, axis=1), nstates, axis=2)
        velocities = velocities + \
            np.multiply(r0, (primes - positions)) + \
            np.multiply(r1, (optimus - positions))
        # clip positions to be within search space
        positions = np.clip(positions + velocities, min_time, max_time)
        # clip velocities to be within allowed limits,
        # done after update to hit limit
        velocities = np.clip(velocities, -max_velocity, max_velocity)
        for i in range(nparticles):
            score = run_sumo(n_intersections, 'summary.xml', positions[i], "pso")
            if score < primals[i]:
                primes[i] = positions[i]
                primals[i] = score
                if score < optimal:
                    optimus = np.tile(positions[i], (nparticles, 1, 1))
                    optimal = score
                    print("%d, %d, %.5f\n" % (t, i, optimal), file=fh)
                    print("%d, %d\n" % (t, i), file=fh3)
                    for row in optimus[0]:
                        print(row, file=fh3)
        print("%d " % t, file=fh2)
        print(primals, "\n", file=fh2)


def main(arguments):
    global args
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument(
        'nparticles', help="number of particles", type=int, default=25)
    parser.add_argument(
        'niters', help="number of iterations", type=int, default=1000)
    parser.add_argument('c0', help="number of iterations",
                        type=float, default=2.)
    parser.add_argument('c1', help="number of iterations",
                        type=float, default=2.)
    parser.add_argument('predfile', help="file to write to",
                        type=str, default="pso")
    parser.add_argument(
        'min_time', help="number of iterations", type=float, default=5.)
    parser.add_argument(
        'max_time', help="number of iterations", type=float, default=30.)
    parser.add_argument(
        'max_velocity', help="number of iterations", type=float, default=10.)
    parser.add_argument(
        'n_intersections', help="number of intersections (n*n grid)", type=int, default=1)
    args = parser.parse_args(arguments)
    nparticles = args.nparticles
    niters = args.niters
    c0 = args.c0
    c1 = args.c1
    n_intersections = args.n_intersections
    min_time = args.min_time
    max_time = args.max_time
    max_velocity = args.max_velocity
    predfile = args.predfile
    pso(nparticles, niters, c0, c1, n_intersections, predfile, min_time, max_time, max_velocity)


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
