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

from population import Population

class SimpleGA(object):

    def __init__(self, N, ngen, nx, p_mate, p_mut, verbose):
        # population size, make it so there is an even number of parents to mate
        if N % 2 == 1:
            N += 1

        self.N = N

        # cap on the number of generations to run
        self.ngen = ngen

        # number of crossover points
        self.nx = nx

        # probability of mating
        self.p_mate = p_mate

        # probability of mutation
        self.p_mut = p_mut

        # container for elite individuals from populations
        self.elite = []

        self.verbose = verbose

    def evolve(self, score, guitar):
        '''
        Begin the genetic algorithm.
        '''

        for seg in score.segments:
            # play god and create a new random population
            pop = Population(self.N, seg, guitar)

            for gen in xrange(self.ngen):
                pop.next_generation(self.nx, self.p_mate, self.p_mut)

                if self.verbose:
                    print "generation %d; fitness: %f" % (gen + 1, pop.calc_fitness())

            # get the elite tab
            self.elite.append(pop.get_elite())

        return self.elite

    def save_elite(self, input_path, output_path):
        pass
