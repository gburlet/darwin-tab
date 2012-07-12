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

from __future__ import division
import sys
sys.path.append('..')
import random as rnd
import copy
from operator import attrgetter

from guitar.guitar import Guitar
from chromosome import Chromosome
from utilities import WeightedRandomGenerator

class Population(object):
    '''
    A population is a collection of guitar tablatures (chromosomes)
    corresponding to the input score.
    '''

    def __init__(self, N, segment, guitar):
        '''
        Instantiate a new population

        PARAMETERS
        ----------
        N {int}: population size
        '''

        self.N = N
        self.guitar = guitar
        self.chromosomes = []

        self._randomize(segment)
        self._assess_individuals()

    def _randomize(self, segment):
        '''
        Create a new population of possible tablatures for the segment of music
        of size N.
        '''

        for i in xrange(self.N):
            chromo = Chromosome(segment, self.guitar)
            self.chromosomes.append(chromo)

    def next_generation(self, nx, p_mate, p_mut):       
        pop_fitness = self.calc_fitness()
        pdf = map(lambda c: c.fitness/pop_fitness, self.chromosomes)
        w_rnd = WeightedRandomGenerator(pdf)

        # cache the parent chromosomes since we're drawing with replacement
        parent_chromos = copy.deepcopy(self.chromosomes)

        # begin breeding the next generation
        for i in xrange(0,self.N,2):
            # select parents with replacement, careful not to change contents of parents
            r = w_rnd.random()
            x = copy.deepcopy(parent_chromos[r])
            y = copy.deepcopy(parent_chromos[w_rnd.random()])

            self.chromosomes[i], self.chromosomes[i+1] = self._breed_parents(x, y, nx, p_mate, p_mut)

        # calculate the fitness of the new population
        self._assess_individuals()

    def _assess_individuals(self):
        # calculate fitness for each chromosome
        for c in self.chromosomes:
            c.calc_fitness()

    def _breed_parents(self, x, y, nx, p_mate, p_mut):
        if rnd.random() < p_mate:
            # get random locus points
            locus = [rnd.randint(0,len(x.genes)-1) for i in range(nx)]
            locus.sort()
            locus.append(len(x.genes)-1)

            # twist about these locus points to form children
            prev_l = 0
            for l in locus:
                if l % 2 == 0:
                    x.genes[prev_l:l] = y.genes[prev_l:l]
                prev_l = l

        if rnd.random() < p_mut:
            self._mutate_chromosome(x)
            self._mutate_chromosome(y)

        return x, y

    def _mutate_chromosome(self, chromo):
        # get random gene to mutate
        g = rnd.choice(chromo.genes)
        g.mutate()

    def calc_fitness(self):
        '''
        Find fitness of this Population
        '''

        return reduce(lambda x,y: x+y, map(lambda c: c.fitness, self.chromosomes))

    def get_elite(self):
        '''
        Return the individual that has the highest fitness
        '''

        return max(self.chromosomes, key=attrgetter('fitness'))
