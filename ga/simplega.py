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
import sys
sys.path.append('..')

from guitar.guitarevent import Strum, Pluck
from score.scoreevent import Note, Chord
from pymei import XmlExport


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
        self.elites = []

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
            self.elites.append(pop.get_elite())
            print self.elites[-1]

        return self.elites

    def save_elite(self, score, output_path):
        '''
        Save the elite tablature to the specified output path.
        At this point, the output file should be a copy on the HDD
        of the original input file, to preserve meta-data and other 
        contents of the file not maintained in the internal representation
        of the musical document.

        PARAMETERS
        ----------
        output_path {String}: the output path of the mei file
        '''

        # get list of tablature data to append to note elements
        # plucks is a list of tuples (MeiElement.id, Pluck)
        plucks = []
        for chromo in self.elites:
            for g in chromo.genes:
                if isinstance(g.guitar_event, Pluck):
                    plucks.append((g.score_event.id, g.guitar_event))
                elif isinstance(g.guitar_event, Strum):
                    for p, n in zip(g.guitar_event.plucks, g.score_event.notes):
                        plucks.append((n.id, p))       
        
        # add the tablature data to the original mei document
        for p in plucks:
            note = score.meidoc.getElementById(p[0])
            note.addAttribute('tab.string', str(p[1].string+1))
            note.addAttribute('tab.fret', str(p[1].fret))

        # write the modified document to disk
        XmlExport.meiDocumentToFile(score.meidoc, output_path)
