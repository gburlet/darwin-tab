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

import sys
sys.path.append('..')

from guitar.guitar import Guitar
from chromosome import Chromosome

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

        self._randomize(segment, guitar)

    def _randomize(self, segment, guitar):
        '''
        Create a new population of possible tablatures for the segment of music
        of size N.
        '''

        for i in xrange(self.N):
            chromo = Chromosome(segment, guitar)
            self.chromosomes.append(chromo)
