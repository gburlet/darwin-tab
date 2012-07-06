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

from score.note import Note

class Guitar:

    tunings = {
        'standard': [Note('E', 4), Note('B', 3), Note('G', 3), Note('D', 3), Note('A', 2), Note('E', 2)],
        'drop_d': [Note('E', 4), Note('B', 3), Note('G', 3), Note('D', 3), Note('A', 2), Note('D', 2)]
    }

    def __init__(self, num_frets=22, tuning='standard'):
        self.num_frets = num_frets 
        if tuning in Guitar.tunings:
            self.tuning = tuning
            self.strings = Guitar.tunings[self.tuning]
        else:
            raise ValueError('Invalid tuning')

    def get_candidate_frets(self, note):
        '''
        Given a note, get all the candidate (string, fret) pairs
        where it could be played given the current guitar properties
        (number of strings, and tuning).
        '''

        candidates = []
        num_chroma = len(Note.pitch_classes)

        for i, s in enumerate(self.strings):
            # calculate pitch difference from the open string note
            oct_diff = note.oct - s.oct
            pname_diff = Note.pitch_classes.index(note.pname) - Note.pitch_classes.index(s.pname)
            pitch_diff = pname_diff + num_chroma*oct_diff

            if pitch_diff >= 0 and pitch_diff <= self.num_frets:
                candidates.append((i, pitch_diff))

        return candidates

    def get_note(self, string, fret):
        '''
        Given a string and fret, return the pitch name and octave
        of the note that would be produced in the current tuning.
        '''

        if fret < 0 or fret > self.num_frets:
            return None

        num_chroma = len(Note.pitch_classes)
        str_note = self.strings[string]
        oct_diff = int(fret/num_chroma)
        i_str_pname = Note.pitch_classes.index(str_note.pname)
        i_note_pname = (i_str_pname + fret) % num_chroma
        if i_note_pname < i_str_pname:
            oct_diff += 1

        pname = Note.pitch_classes[i_note_pname]
        oct = str_note.oct + oct_diff

        return Note(pname, oct)

    def __str__(self):
        return "<Guitar: %d frets, %s tuning>" % (self.num_frets, self.tuning)