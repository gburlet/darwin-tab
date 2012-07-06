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

from scoreevent import Note

class Score(object):

    def __init__(self, filename):
        '''
        Initialize a score. Fill the score with notes
        parsed from the provided file
        '''

        # input filename
        self.filename = filename

        # segments of music
        self.segments = []

        #self.parseInput(segment=False)

        # for now, fill the score with fake data
        # C Major scale
        oct = 3
        pnames = ['C','D','E','F','G','A','B']
        notes = []
        for pname in pnames:
            notes.append(Note(pname,oct))
        notes.append(Note('C',oct+1))
        self.segments.append(notes)

    def parseInput(self, segment=False):
        '''
        Fill segments of music with notes and chords.

        PARAMETERS
        ----------
        segment {Boolean}: perform auto segmentation to the musical score
        '''
        pass
