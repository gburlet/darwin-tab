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

from guitar.guitarevent import Strum, Pluck
from score.scoreevent import Note, Chord
from random import choice

class Gene:
    '''
    A Gene represents a chord---multiple notes occuring simultaneously.
    The allele for a gene is one strum (up to 6 plucks - maximum polyphony of the guitar)
    each describing the fret position and string to pluck.
    '''

    def __init__(self, score_event, guitar):
        self.guitar = guitar
        self.score_event = score_event
        self.guitar_event = None

        self._randomize()

    def _randomize(self, diff_alleles=False):
        '''
        Select random plucks on the guitar model that would
        produce the given pitches in the score event.

        PARAMETERS:
            diff_alleles {boolean}: if the alleles have already been chosen
                                    for the gene, make sure they are different.
        '''

        if isinstance(self.score_event, Chord):
            plucks = []
            for i, n in enumerate(self.score_event.notes):
                candidates = self.guitar.get_candidate_frets(n)
                if self.guitar_event is not None and diff_alleles:
                    # ensure alleles are different
                    candidates = filter(lambda p: p != self.guitar_event.plucks[i], candidates)
                plucks.append(choice(candidates))
            self.guitar_event = Strum(plucks)
        elif isinstance(self.score_event, Note):
            candidates = self.guitar.get_candidate_frets(self.score_event)
            if self.guitar_event is not None and diff_alleles:
                # ensure alleles are different
                candidates = filter(lambda p: p != self.guitar_event, candidates)
            self.guitar_event = choice(candidates)

    def mutate(self):
        self._randomize(diff_alleles=True)

    def __str__(self):
        return "<gene %s>" % self.guitar_event
