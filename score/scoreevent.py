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

class Chord:

    def __init__(self, notes):
        self.set_notes(notes)

    def add_note(self, note):
        self.notes.append(note)

    def del_note(self, pname, oct):
        note = Note(pname, oct)
        self.notes = filter(lambda n: n != note, self.notes)

    def set_notes(self, notes):
        self.notes = notes

class Note:

    pitch_classes = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']

    def __init__(self, pname, oct, **kwargs):
        # pitch class
        if pname.upper() in Note.pitch_classes:
            self.pname = pname.upper()
        else:
            raise ValueError('Invalid pitch name')

        # octave
        self.oct = oct

        # optional timing information
        # timestamp start
        self.ts_start = kwargs.get('ts_start')
        # beat start
        self.beat_start = kwargs.get('beat_start')
        # beat duration
        self.dur = kwargs.get('dur')

    def __eq__(self, other_note):
        return self.pname == other_note.pname and self.oct == other_note.oct

    def __str__(self):
        return "<note: %s%d>" % (self.pname, self.oct)
