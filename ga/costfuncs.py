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

from darwintab.guitar.guitarevent import Strum, Pluck

def biomechanical_burlet(chromo):
    '''
    Evaluate the cost of a chromosome according to the minimum distance
    between frets and a preference for lower fret numbers
    '''        

    distance = 0            # biomechanical distance
    w_distance = 1          # distance weight
    
    for i in xrange(1,len(chromo.genes)):
        prev_strum = chromo.genes[i-1].guitar_event
        cur_strum = chromo.genes[i].guitar_event

        # calculate distance between the two events
        distance += prev_strum.distance(cur_strum)

    fret_penalty = 0
    w_fret_penalty = 2      # fret penalty weight
    fret_threshold = 7      # start incurring penalties above fret 7

    chord_distance = 0
    w_chord_distance = 1

    for g in chromo.genes:
        cur_strum = g.guitar_event
        if isinstance(cur_strum, Pluck):
            if cur_strum.fret > fret_threshold:
                fret_penalty += 1
        else:
            frets = [p.fret for p in cur_strum.plucks]
            if max(frets) > fret_threshold:
                fret_penalty += 1

            chord_distance += max(frets) - min(frets)

    return w_distance*distance + w_fret_penalty*fret_penalty + w_chord_distance*chord_distance

def biomechanical_tuohy(chromo):
    '''
    Evaluate the cost of a given chromosome according
    to biomechanical constraints, which assess the physical
    difficulty of hand movement.
    From tuohy2009 - Guitar Tablature Creation with Neural Networks
                     and Distributed Genetic Search

    (+ cost)
    Fret Distances
    --------------
    1. number of frets depressed
    2. total fretwise distance between sequential chords + penalty for large distance
    3. total fretwise distance between each chord and average of 6 surrounding notes + penalty for large distance
    4. total fretwise distance within chords
    5. total largest fretwise distance between any two notes of sequential chords

    Intuitive Penalties
    -------------------
    1. Higher note played on lower string
    2. Lower note played on higher string
    3. Slightly penalize open pluck followed by fretted pluck on higher frets

    Cognitive Penalties
    -------------------
    1. Slight penalty to notes played higher on fretboard
    '''
    
    # factors which inhibit cost
    num_frets_depressed = 0     # number of frets depressed throughout the tab   
    fret_distance_between = 0   # fret distance between consecutive events
    fret_distance_context = 0   # fret distance between event and average of 6 surrounding events
    fret_distance_within = 0    # fret distance within chords
    fret_distance_largest = 0   # largest fretwise distance between notes of sequential chords
    intuitive_penalty = 0       # intuitive costs (higher notes played on thinner strings)
    cognitive_penalty = 0       # cognitive costs (high notes played higher on fretboard)

    #num_open_strings = 0

    # weights
    w_num_frets_depressed = 1.0  
    w_fret_distance_between = 2.0  
    w_fret_distance_context = 4.0
    w_fret_distance_within = 2.0
    w_fret_distance_largest = 2.0
    w_cognitive_penalty = 2.0
    w_intuitive_penalty = 1.5

    for i in xrange(len(chromo.genes)):
        # get six surrounding events (3 before, current, 3 after)
        context = []
        for j in range(-3,4):
            # get 3 previous events
            event = chromo.genes[i+j].guitar_event if i+j >= 0 and i+j < len(chromo.genes) else None

            if isinstance(event, Pluck):
                context.append([event])
            elif isinstance(event, Strum):
                context.append(event.plucks)

        # these variables are for code readability
        cur_strum = context[3]
        prev_strum = context[2]

        cur_frets_depressed = filter(lambda f: f != 0, [p.fret for p in cur_strum])

        #num_open_strings += len(cur_strum) - len(cur_frets_depressed)
        num_frets_depressed += len(cur_frets_depressed)

        if len(cur_frets_depressed) > 0:
            fret_avg = reduce(lambda f1,f2: f1+f2, cur_frets_depressed)/len(cur_frets_depressed)

            # calculate how much the chord frets deviate from the average fret number in the chord
            fret_distance_within += reduce(lambda f1,f2: f1+f2, map(lambda f: abs(f - fret_avg), cur_frets_depressed))
                    
            # calculate average fret-wise distance between chords in context
            context_frets_depressed = {'sum': 0, 'len': 0} # more efficient than pushing to a list to find avg
            for strum in context:
                if strum is cur_strum:
                    # distance with itself is always zero
                    continue

                if strum is not None:
                    strum_frets_depressed = filter(lambda f: f != 0, [p.fret for p in strum])
                    context_frets_depressed['sum'] += sum(strum_frets_depressed)
                    context_frets_depressed['len'] += len(strum_frets_depressed)

                    if strum is prev_strum and len(strum) == 1 and len(cur_strum) == 1 and cur_strum[0].fret > 5:
                        # penalize an open pluck followed by a fretted pluck
                        if prev_strum[0].fret == 0 and cur_strum[0].fret != 0:
                            intuitive_penalty += 5

                        # check if higher note is played on a lower string
                        # or lower note is played on a higher string
                        prev_note = chromo.genes[i-1].score_event
                        cur_note = chromo.genes[i].score_event
                        #if cur_note > prev_note and cur_strum[0].string < prev_strum[0].string:
                        #    intuitive_penalty += 10
                        #elif cur_note < prev_note and cur_strum[0].string > prev_strum[0].string:
                        #    intuitive_penalty += 10

                    if len(strum_frets_depressed) > 0:
                        strum_fret_avg = sum(strum_frets_depressed)/len(strum_frets_depressed)
                        strum_distance = sum(map(lambda f: abs(f - strum_fret_avg), cur_frets_depressed))

                        # slight penalty to notes played high on the fretboard
                        if strum_fret_avg > 8:
                            cognitive_penalty += 10

                        if strum is prev_strum:
                            # add fret-wise distance between previous strum to cost function
                            fret_distance_between += strum_distance

                            # add penalty for excessively large fret-wise distances
                            if strum_distance > 5 * len(strum_frets_depressed): 
                                # since 5 frets is span of hand
                                w_fret_distance_between *= 2

                            # total largest fretwise distance between any two notes of sequential chords
                            max_seq_fret_distance = 0
                            for p_cur in cur_strum:
                                for p_prev in prev_strum:
                                    notewise_distance = abs(p_cur.fret - p_prev.fret)
                                    if notewise_distance > max_seq_fret_distance:
                                        max_seq_fret_distance = notewise_distance

                            fret_distance_largest += max_seq_fret_distance

            context_fret_avg = context_frets_depressed['sum']/context_frets_depressed['len']
            context_distance = sum(map(lambda f: abs(f - context_fret_avg), cur_frets_depressed))
            fret_distance_context += context_distance

            # add penalty for excessively large context fret-wise differences
            if context_distance > 5 * len(cur_frets_depressed):
                # since 5 frets is span of hand
                w_fret_distance_context *= 2

            # add penalty for 

    cost = (w_num_frets_depressed*num_frets_depressed
            + w_fret_distance_within*fret_distance_within 
            + w_fret_distance_between*fret_distance_between
            + w_fret_distance_largest*fret_distance_largest
            + w_fret_distance_context*fret_distance_context
            + w_intuitive_penalty*intuitive_penalty
            + w_cognitive_penalty*cognitive_penalty)

    return cost


