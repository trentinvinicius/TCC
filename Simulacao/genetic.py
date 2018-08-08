from random import randint, choice, randrange, random
import struct
from constants import *
from operator import itemgetter

NUMBER = 0
MAXIMIZE, MINIMIZE = 11, 22

class Individual():
    alleles = (0, 1)
    def __init__(self, chromosome):
    	self.chromosome = chromosome or self._makechromosome()
    	self.score = None  # set during evaluation
    	self.allData = []  # vector to store the data from the genetic algorithm 
    	#self.num = num

    def _makechromosome(self):
        global NUMBER
        #"makes a chromosome from randomly selected alleles."
        chromosome = [choice(self.alleles) for gene in range(self.length)]
        if NUMBER < NUMMAXBRAKE: # set the brake force to maximum
            chromosome[:self.bits_per_gene] = [1 for i in range(self.bits_per_gene)]
        NUMBER += 1
        return chromosome

    @property
    def score(self):
    	return self.score

    @score.setter
    def score(self, value):
    	self.score = value

    def decode(self, i, gene_min, gene_max, integer):
    	bin_gene = ''
    	for bit in self.chromosome[i * self.bits_per_gene : (i + 1) * self.bits_per_gene]:
    		if bit:
    			bin_gene += '1'
    		else:
    			bin_gene += '0'
    	int_gene = int(bin_gene, 2)			        
    	float_gene = float(int_gene) / (2**self.bits_per_gene)
    	gene = gene_min + float_gene*(gene_max - gene_min) 
    	if integer:
    		gene = int(round(gene))
    	return gene

    def crossover(self, other):
        #"override this method to use your preferred crossover method."
    	return self._twopoint(other)

    def mutate(self, gene):
        #"override this method to use your preferred mutation method."
        self._pick(gene) 

    # sample mutation method
    def _pick(self, gene):
        #"chooses a random allele to replace this gene's allele."
        self.chromosome[gene] = choice(self.alleles)

    # sample crossover method
    def _twopoint(self, other):
        #"creates offspring via two-point crossover between mates."
        left, right = self._pickpivots()
        def mate(p0, p1):
            chromosome = p0.chromosome[:]
            chromosome[left:right] = p1.chromosome[left:right]
            child = p0.__class__(chromosome)
            child._repair(p0, p1)
            return child
        return mate(self, other), mate(other, self)

    # some crossover helpers ...
    def _repair(self, parent1, parent2):
        #"override this method, if necessary, to fix duplicated genes."
        pass

    def _pickpivots(self):
        left = randrange(1, self.length-2)
        right = randrange(left, self.length-1)
        return left, right

    #
    # other methods
    #

    def __repr__(self):
        #"returns string representation of self"
        chromosome_str = ''
        for gene in self.chromosome:
                if gene:
                        chromosome_str += '1'
                else:
                        chromosome_str += '0'
        return '<%s chromosome="%s" score=%s>' % \
               (self.__class__.__name__,
                chromosome_str, self.score)

    def __cmp__(self, other):
        if self.optimization == MINIMIZE:
            return cmp(self.score, other.score)
        else: # MAXIMIZE
            return cmp(other.score, self.score)

    def copy(self):
        twin = self.__class__(self.chromosome[:])
        twin.score = self.score
        return twin




class GeneticAlgorithm(object):
    def __init__(self, kind, population=None, size=100, maxgenerations=2, \
                 generation=0, crossover_rate=0.90, mutation_rate=0.02, \
                 optimum=None, island = None):
        self.kind = kind
        self.size = size
        self.optimum = optimum
        self.island = island
        if population == None:
            self.population = self._makepopulation()
        elif len(population) < size:
            self.population = population + self._makepopulation(size - len(population))
        else:
            self.population = population
        #self.population = population or self._makepopulation()
        self.population.sort(key = lambda x: x.score, reverse = True)
        for n, individual in enumerate(self.population):
            individual.evaluate(n, self.island, generation)
            if individual.score == self.optimum:
            	break
        self.population.sort(key = lambda x: x.score, reverse = True)
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.maxgenerations = maxgenerations
        self.generation = generation
        self.hasConverged = False
        self.report()

    def _makepopulation(self, num = None):
        return [self.kind() for individual in range(num or self.size)]
    
    def run(self):
        while not self._goal():
        	self.step()
    
    def _goal(self):
        return self.generation >= self.maxgenerations or \
               self.best.score == self.optimum or self.hasConverged
    
    def step(self):
        self.population.sort(key = lambda x: x.score, reverse = True)
        self._crossover()
        self.population.sort(key = lambda x: x.score, reverse = True)
        self.generation += 1
        self.report()
        
    
    def _crossover(self):
        next_population = [self.best.copy()]
        stop = False
        while len(next_population) < self.size and not stop:
            mate1 = self._select()
            if random() < self.crossover_rate:
                mate2 = self._select()
                offspring = mate1.crossover(mate2)
            else:
                offspring = [mate1.copy()]
            for individual in offspring:
                self._mutate(individual)
                individual.evaluate(len(next_population), self.island, self.generation)                
                next_population.append(individual)
                if individual.score == self.optimum:
                    individual.evaluate(len(next_population), self.island, self.generation, True)
                    if individual.score == self.optimum:
                            stop = True
                            break
        self.population = next_population[:self.size]

    def _select(self):
        "override this to use your preferred selection method"
        return self._tournament()
    
    def _mutate(self, individual):
        for gene in range(individual.length):
            if random() < self.mutation_rate:
                individual.mutate(gene)

    #
    # sample selection method
    #
    def _tournament(self, size=8, choosebest=0.90):
        competitors = [choice(self.population) for i in range(size)]
        competitors.sort(key = lambda x: x.score, reverse = True)
        if random() < choosebest:
            return competitors[0]
        else:
            return choice(competitors[1:])
    
    def best():
        doc = "individual with best fitness score in population."
        def fget(self):
            return self.population[0]
        return locals()
    best = property(**best())

    def report(self):
        print "="*70
        print "generation: ", self.generation
        print "best:       ", self.best
        print "="*70
