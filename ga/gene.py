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
    The allele for a gene is up to 6 integers (maximum polyphony of the guitar)
    each describing the fret position.
    '''

    def __init__(self, event, guitar):
        self.guitar = guitar

        self._randomize(event, guitar)

    def _randomize(self, event, guitar):
        if isinstance(event, Chord):
            plucks = []
            for n in event.notes:
                pluck.append(choice(guitar.get_candidate_frets(n)))
            self.event = Strum(plucks)
        elif isinstance(event, Note):
            self.event = choice(guitar.get_candidate_frets(event))

    def __str__(self):
        return "<gene %s>" % self.event
