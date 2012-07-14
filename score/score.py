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

from pymei import MeiDocument, MeiElement, XmlImport
from scoreevent import Note, Chord

class Score(object):

    def __init__(self, input_path):
        '''
        Initialize a score. Fill the score with notes
        parsed from the provided file
        '''

        # input filename
        self.input_path = input_path

        # segments of music
        self.segments = []

        self.parseInput(segment=True)

    def parseInput(self, segment=True):
        '''
        Fill segments of music with notes and chords.

        PARAMETERS
        ----------
        segment {Boolean}: segment the musical score on mei section elements
        '''
        
        # read in the Mei document
        self.meidoc = XmlImport.read(self.input_path)
        mei = self.meidoc.getRootElement()

        sections = mei.getDescendantsByName('section')
        for s in sections:
            segment = []
            # get measures in section
            measures = s.getChildrenByName('measure')
            for m in measures:
                # only parse first staff (instrument), the instrument to convert to tablature
                staff = m.getChildrenByName('staff')[0]
                # only parse first layer (assume only one voice)
                layer = staff.getChildrenByName('layer')[0]
                score_events = layer.getChildren()
                for e in score_events:
                    if e.getName() == 'chord':
                        notes_in_chord = [Note(n.getAttribute('pname').value, int(n.getAttribute('oct').value), n.getId()) 
                                         for n in e.getChildrenByName('note')]
                        chord = Chord(notes_in_chord)
                        segment.append(chord)
                    elif e.getName() == 'note':
                        note = Note(e.getAttribute('pname').value, int(e.getAttribute('oct').value), e.getId())
                        segment.append(note)

            self.segments.append(segment)

                            

                
