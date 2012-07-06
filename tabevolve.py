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

from ga.simplega import SimpleGA

# set up command line argument structure
parser = argparse.ArgumentParser(description='Convert a MIDI file to tablature using a genetic algorithm.')
parser.add_argument('-p', '--popsize', type=int, help='population size')
parser.add_argument('-pmate', '--mateprob', type=float, help='probability the parents will mate')
parser.add_argument('-pmut', '--mutateprob', type=float, help='probability of mutation')
parser.add_argument('-nx', '--ncross', type=int, help='number of crossover points when mating')
parser.add_argument('-ngen', '--numgeneration', type=int, help='cap on the number of iterations')
parser.add_argument('-fin', '--filein', help='input file')
parser.add_argument('-fout', '--fileout', help='output file')
parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')

def main():
    # parse command line arguments
    args = parser.parse_args()

    # start up the genetic algorithm
    ga = SimpleGA(args.popsize, args.numgeneration, args.ncross, args.mateprob, args.mutateprob)

if __name__ == '__main__':
    main()
