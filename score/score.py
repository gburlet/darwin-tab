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

        self.parseInput(segment=False)

    def parseInput(self, segment=False):
        '''
        Fill segments of music with notes and chords.

        PARAMETERS
        ----------
        segment {Boolean}: perform auto segmentation to the musical score
        '''

class Segment(object):
    '''
    A segment of music is a grouping of score events (notes or chords)
    which are assigned guitar events (plucks or strums)
    '''

    def __init__(self, score_events):
        self.events = score_events
