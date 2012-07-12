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

from gene import Gene
from costfuncs import *

class Chromosome:
    '''
    A chromosome represents a string of genes. In this application, a chromosome
    represents a phrase of tablature, which contains a sequence of genes (chords).
    '''

    def __init__(self, segment, guitar):
        self.guitar = guitar
        
        # initialize with empty sequence of genes
        self.genes = []

        # fitness of the chromosome
        self.fitness = 0

        self._randomize(segment, guitar)

    def _randomize(self, segment, guitar):
        for event in segment:
            gene = Gene(event, guitar)
            self.genes.append(gene)

    def calc_fitness(self):
        cost = biomechanical_cost(self)
        self.fitness = 1.0/(cost + 1.0)

    def __str__(self):
        return "\n".join(map(lambda g: g.__str__(), self.genes))
