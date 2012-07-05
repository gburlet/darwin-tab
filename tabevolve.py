import argparse

# set up command line argument structure
parser = argparse.ArgumentParser(description='Convert a MIDI file to tablature using a genetic algorithm.')
parser.add_argument('-p', '--popsize', type=int, help='population size')
parser.add_argument('-pmate', '--mateprob', type=float, help='probability the parents will mate')
parser.add_argument('-pmut', '--mutateprob', type=float, help='probability of mutation')
parser.add_argument('-nx', '--ncross', type=int, help='number of crossover points when mating')
parser.add_argument('-ngen', '--numgeneration', type=int, help='cap on the number of iterations')
parser.add_argument('-fin', '--filein', help='input file')
parser.add_argument('-fout', '--fileout', help='output file')
parser.add_argument('-v', '--verbose', help='increase output verbosity', action='store_true')

def main():
    args = parser.parse_args()

if __name__ == '__main__':
    main()
