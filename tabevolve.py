'''
Copyright (c) 2012 Gregory Burlet

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import argparse
import os

from darwintab.ga.simplega import SimpleGA
from darwintab.guitar.guitar import Guitar
from darwintab.score.score import Score
import time

# set up command line argument structure
parser = argparse.ArgumentParser(description='Convert a Mei file to tablature using a genetic algorithm.')
parser.add_argument('-p', '--popsize', type=int, help='population size')
parser.add_argument('-pmate', '--mateprob', type=float, help='probability the parents will mate')
parser.add_argument('-pmut', '--mutateprob', type=float, help='probability of mutation')
parser.add_argument('-nx', '--ncross', type=int, help='number of crossover points when mating')
parser.add_argument('-ngen', '--numgeneration', type=int, help='cap on the number of iterations')
parser.add_argument('-nf', '--numfrets', type=int, help='number of frets on the guitar')
parser.add_argument('-t', '--tuning', choices=['standard', 'drop_d'], default='standard', help='tuning of your guitar')
parser.add_argument('-c', '--capo', type=int, help='capo fret number')
parser.add_argument('filein', help='input file')
parser.add_argument('fileout', help='output file')
parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')

def print_timing(func):
    def wrapper(*arg):
        t1 = time.time()
        res = func(*arg)
        t2 = time.time()
        print '%s took %0.2f s' % (func.func_name, (t2-t1))
        return res
    return wrapper

@print_timing
def arrange_tab():
    # parse command line arguments
    args = parser.parse_args()

    # instantiate a model of the guitar the user is using
    guitar = Guitar(args.numfrets, args.tuning, args.capo)

    if not os.path.exists(args.filein):
        raise ValueError('The input file does not exist')
    _, input_ext = os.path.splitext(args.filein)
    if input_ext != '.mei':
        raise ValueError('The input file must be in mei file format')

    # generate the score model
    score = Score()
    score.parse_mei_file(args.filein)
    
    # start up the genetic algorithm
    ga = SimpleGA(args.popsize, args.numgeneration, args.ncross, args.mateprob, args.mutateprob, args.verbose)

    # create tablature for the guitar with the given parameters
    ga.evolve(score, guitar)
    
    # save the elites to the output file
    ga.save_elite(score, args.fileout)

if __name__ == '__main__':
    arrange_tab()
