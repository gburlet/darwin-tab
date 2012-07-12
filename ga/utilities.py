import random as rnd
import bisect as bs

class WeightedRandomGenerator(object):

    def __init__(self, pdf):
        self.cdf = pdf[:]

        for i, p in enumerate(self.cdf):
            if i > 0:
                self.cdf[i] += self.cdf[i-1]

    def random(self):
        r = rnd.random()
        return bs.bisect_right(self.cdf, r)

    def __call__(self):
        return self.next()
