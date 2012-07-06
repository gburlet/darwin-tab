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

class GuitarEvent(object):

    def __init__(self, **kwargs):
        # optional timing information
        # timestamp start
        self.ts_start = kwargs.get('ts_start')
        # beat start
        self.beat_start = kwargs.get('beat_start')
        # beat duration
        self.dur = kwargs.get('dur')

class Strum(GuitarEvent):

    def __init__(self, plucks, **kwargs):
        '''
        kwargs is for passing in timing information
        '''
        super(Chords, self).__init__(**kwargs)

        self._set_plucks(plucks)

    def add_pluck(self, pluck):
        self.plucks.append(pluck)

    def del_pluck(self, string, fret):
        pluck = Pluck(string, fret)
        self._plucks = filter(lambda n: n != pluck, self.plucks)

    def _get_plucks(self):
        return self._plucks

    def _set_plucks(self, plucks):
        self._plucks = plucks

    plucks = property(_get_plucks, _set_plucks)

    def __str__(self):
        return "<strum: %s>" % ", ".join(self._plucks)

class Pluck(GuitarEvent):

    def __init__(self, string, fret, **kwargs):
        super(Pluck, self).__init__(**kwargs)

        self.string = string
        self.fret = fret

    def __eq__(self, other_pluck):
        return self.string == other_pluck.string and self.fret == other_pluck.fret
