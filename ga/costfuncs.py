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

from __future__ import division
import sys
sys.path.append('..')

from guitar.guitarevent import Strum, Pluck

def biomechanical_cost(chromo):
    '''
    Evaluate the cost of a given chromosome according
    to biomechanical constraints, which assess the physical
    difficulty of hand movement.
    From tuohy2009 - Guitar Tablature Creation with Neural Networks
                     and Distributed Genetic Search
    '''
    
    # factors which inhibit cost
    num_frets_depressed = 0     # number of frets depressed throughout the tab   
    fret_distance_between = 0   # fret distance between consecutive events
    fret_distance_surround = 0  # fret distance between event and average of 6 surrounding events
    fret_distance_within = 0    # fret distance within chords
    fret_distance_largest = 0   # largest fretwise distance between notes of sequential chords

    # factors which contribute to cost
    num_open_strings = 0

    # weights
    w_num_frets_depressed = 1.0  
    w_fret_distance_between = 1.0  
    w_fret_distance_surround = 1.0
    w_fret_distance_within = 1.0
    w_fret_distance_largest = 1.0
    w_num_open_strings = -1.0

    prev_gene = None
    for i in xrange(chromo.genes):
        # get six surrounding events (3 before, current, 3 after)
        context = []
        for j in range(-3,4):
            # get 3 previous events
            event = chromo.genes[i+j].guitar_event if i+j >= 0 and i+j < len(chromo.genes) else None

            if isinstance(event, Pluck):
                context.append([event])
            elif isinstance(event, Strum):
                context.append(event.plucks)

        # this variable is for code readability
        cur_strum = context[3]

        frets_depressed = filter(lambda f: f != 0, [p.fret for p in cur_strum])

        num_open_strings += len(cur_strum) - len(frets_depressed)
        num_frets_depressed += len(frets_depressed)

        if len(frets_depressed) > 0:
            fret_avg = reduce(lambda f1,f2: f1+f2, frets_depressed)/len(frets_depressed)

            # calculate how much the chord frets deviate from the average fret number in the chord
            fret_distance_within += reduce(lambda f1,f2: f1+f2, map(lambda f: abs(f - fret_avg), frets_depressed))
                    
        # calculate fretwise distance between sequential chords
        if surrounding[2] is not None:
            prev_frets_depressed = filter(lambda f: f != 0, [p.fret for p in surrounding[2]])

    cost = (w_num_frets_depressed*num_frets_depressed + w_num_open_strings*num_open_strings
            + w_fret_distance_within*fret_distance_within + w_fret_distance_between*fret_distance_between)

    return cost
