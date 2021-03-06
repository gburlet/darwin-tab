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

    def __init__(self):
        '''
        Initialize a score 
        '''

        # segments of music
        self.segments = []

    def parse_mei_str(self, mei_str, segment=True):
        '''
        Read an mei file from string and fill the score model
        '''

        self.meidoc = XmlImport.documentFromText(mei_str)
        self.parse_input(segment)

    def parse_mei_file(self, mei_path, segment=True):
        '''
        Read an mei file and fill the score model
        '''

        self.meidoc = XmlImport.documentFromFile(str(mei_path))
        self.parse_input(segment)

    def parse_input(self, segment=True):
        '''
        Fill segments of music with notes and chords.

        PARAMETERS
        ----------
        segment {Boolean}: segment the musical score on mei section elements
        '''
        
        # read in the Mei document
        mei = self.meidoc.getRootElement()

        pitch_names = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
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
                        notes_in_chord = []
                        for n in e.getChildrenByName('note'):
                            note = self._handle_mei_note(n)    
                            notes_in_chord.append(note)
                        chord = Chord(notes_in_chord)
                        segment.append(chord)
                    elif e.getName() == 'note':
                        note = self._handle_mei_note(e)
                        segment.append(note)

            self.segments.append(segment)

    def _handle_mei_note(self, note):
        '''
        Helper function that takes an mei note element
        and creates a Note object out of it.
        '''
        
        pname = note.getAttribute('pname').value
        # append accidental to pname for internal model
        if note.hasAttribute('accid.ges'):
            accid = note.getAttribute('accid.ges').value
            if accid == 'f':
                # convert to sharp
                pname = pitch_names[pitch_names.index(pname)-1 % len(pitch_names)] + '#'
            if accid == 's':
                pname += '#'
        oct = int(note.getAttribute('oct').value)
        id = note.getId()

        return Note(pname, oct, id)

