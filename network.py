import datetime
import math
import random
import unittest
from itertools import chain

import genetic



#
#    n1 ----- s1------s2-------s3------s4 ----- n2
#             s1---------------s3
#                     s2---------------s4
#             s1------s5-------s6------s4
#

# a = 1
# b = 1
# c = 1

def is_valid_Path(path,network):

    for x in range(0,len(path)-1):
        if path[x+1] in network[path[x]]:
            continue
        else:
            return 0

    return 1

def get_fitness(path,bandwidth,delay,network):

    min = -1
    connectedNodes = 0
    path2 = path[1:-1]


    for switch in path2:
        if min==-1:
            min = bandwidth[switch]
        else:
            if(bandwidth[switch]<min):
                min = bandwidth[switch]

    for x in range(0,len(path)-1):
        if(path[x+1] in network[path[x]]):
            connectedNodes = connectedNodes + 1

    if connectedNodes == len(path)-1:
        isvalidpath = 1
    else:
        isvalidpath = 0
    total_delay = 0
    if isvalidpath:
        for x in range(0,len(path)-1):
            total_delay+=delay[path[x]][path[x+1]]
    else:
        total_delay = 5000

    return Fitness(connectedNodes,min,total_delay,isvalidpath);

class Fitness:

    connectedNodes = 0
    bandwidth = 0
    isValidPath = -1
    delay = 0
    jitter = 0


    def __init__(self,connectedNodes,bandwidth,delay,isValidPath):
        self.connectedNodes = connectedNodes
        self.bandwidth = bandwidth
        self.isValidPath = isValidPath
        self.delay = delay
        # self.jitter = jitter



def mutate(path,network):
    index = random.randrange(1, len(path)-1)
    path2 = path[:]

    altIndex = random.randrange(1, len(network['switches']))

    i=0
    while network['switches'][altIndex] in path:
        altIndex = random.randrange(1, len(network['switches']))
        i=i+1
        if i==100:
            break
    if i==100:
        return path2

    path2[index] = network['switches'][altIndex]

    return path2


def crossover(path1,path2):
    commonPointx = -1
    commonPointy = -1

    for x in range(1,len(path1)-1):
        flag = 0
        for y in range(1,len(path2)-1):
            if (path1[x]==path2[y]):
                commonPointx = x
                commonPointy = y
                flag=1
                break
        if flag==1:
            break

    if commonPointx == -1:
        print "Crossover not possible"
        return []


    pathTemp = path1[:]
    path1 = path1[:commonPointx]

    for i in range(commonPointy,len(path2)):
        path1.append(path2[i])

    path2 = path2[:commonPointy]

    for i in range(commonPointx,len(pathTemp)):
        path2.append(pathTemp[i])

    # print "path1 is " + str(path1)
    # print "path2 is " + str(path2)

    paths = [path1,path2]

    return paths

class Chromosome:

    def __init__(self,genes,fitness,strategy,age):
        self.genes = genes
        self.fitness = fitness
        self.strategy = strategy
        self.age = age

    def __eq__(self, other):

        for genex in self.genes:
            for geney in other.genes:
                if genex!=geney:
                    return False
        if self.fitness.isValidPath != other.fitness.isValidPath:
            return False

        if self.fitness.connectedNodes != other.fitness.connectedNodes:
            return False

        if self.fitness.bandwidth != other.fitness.bandwidth:
            return False

        return True


a=0.5
b=0.5
req_bw = 4000
req_delay = 4
def calculateFitness(cx):
    x = (a * ((cx.fitness.delay - req_delay) / req_delay))
    y = (b * ((req_bw - cx.fitness.bandwidth) / float (req_bw)))
    valx = (a * ((cx.fitness.delay - req_delay) / float (req_delay))) + (b *  (req_bw - cx.fitness.bandwidth)  / float(req_bw) )
    print("b = "+str(b)+" cx.fitness.bandwidth= "+str(cx.fitness.bandwidth)+" req_bandwidth= "+str(req_bw)+" "+" val= "+str(y))
    print("a = "+ str(a) + " cx.fitness.delay= " + str(cx.fitness.delay) + " req_delay= " + str(req_delay) + " " + " val= " + str(x))
    return valx

def cmp(cx, cy):
    if cx.fitness.isValidPath < cy.fitness.isValidPath:
        return 1
    elif cx.fitness.isValidPath > cy.fitness.isValidPath:
        return -1
    elif cx.fitness.isValidPath == cy.fitness.isValidPath:
        if cx.fitness.isValidPath == 1:

            if calculateFitness(cx) < calculateFitness(cy):
                return -1
            else:
                return 1
        else:
            if cx.fitness.connectedNodes < cy.fitness.connectedNodes:
                return 1
            else:
                return -1

def display(chromosome):

    print "Path is " + str(chromosome.genes)
    print "Fitness: validPath "+ str(chromosome.fitness.isValidPath) + " connectedNodes "+ str(chromosome.fitness.connectedNodes) + " bandwidth "+ str(chromosome.fitness.bandwidth)

def isrepetitivePath(path):
    if len(path) != len(list(set(path))):
        return True
    else:
        return False

class Network:

    def add_link(self,network,src,dst):
        if src in network:
            network[src].append(dst)
        else:
            network[src] = []
            network[src].append(dst)

        if dst in network:
            network[dst].append(src)
        else:
            network[dst] = []
            network[dst].append(src)

    def add_delay(self,delay,src,dst,t):
        delay.setdefault(src,{})
        delay.setdefault(dst,{})
        delay[src][dst] = t
        delay[dst][src] = t

    def test_network(self):
        network = {}
        network['switches'] = []
        # network['switches']=['s1','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','s12','s13','s14']
        # self.add_link(network,'n1','s1')
        # self.add_link(network,'s1','s2')
        # self.add_link(network,'s2','s3')
        # self.add_link(network,'s3','s4')
        # self.add_link(network,'s4','n2')
        #
        # self.add_link(network,'s1','s3')
        # self.add_link(network,'s2','s4')
        #
        # self.add_link(network,'s1','s5')
        # self.add_link(network,'s5','s6')
        # self.add_link(network,'s6','s4')
        #
        # self.add_link(network, 's2', 's7')
        # self.add_link(network, 's7', 's8')
        # self.add_link(network, 's8', 'n2')
        #
        # self.add_link(network, 's9', 'n1')
        # self.add_link(network, 's9', 's2')
        # self.add_link(network, 's9', 's1')
        #
        # self.add_link(network, 'n1', 's10')
        # self.add_link(network, 's10','s11')
        # self.add_link(network, 's11', 'n2')
        #
        # self.add_link(network, 's14', 's13')
        # self.add_link(network, 's13', 's12')
        #
        #
        # bandwidth = {}
        #
        # bandwidth['s1'] = 6000
        # bandwidth['s2'] = 4000
        # bandwidth['s3'] = 500
        # bandwidth['s4'] = 500
        # bandwidth['s5'] = 3000
        # bandwidth['s6'] = 3000
        # bandwidth['s7'] = 4000
        # bandwidth['s8'] = 4000
        # bandwidth['s9'] = 5000
        # bandwidth['s10'] = 6000
        # bandwidth['s11'] = 6000
        # bandwidth['s12'] = 6000
        # bandwidth['s13'] = 6000
        # bandwidth['s14'] = 6000
        #
        # delay = {}
        #
        # delay['n1'] = {}
        # delay['s1'] = {}
        # delay['s2'] = {}
        # delay['s3'] = {}
        # delay['s4'] = {}
        # delay['s5'] = {}
        # delay['s6'] = {}
        # delay['s7'] = {}
        # delay['s8'] = {}
        # delay['s9'] = {}
        # delay['s10'] = {}
        # delay['s11'] = {}
        # delay['s12'] = {}
        # delay['s13'] = {}
        # delay['s14'] = {}

        network['switches'] = ['s1', 's2', 's3', 's4', 's5', 's6', 's7', 's8']

        self.add_link(network,'n1','s1')
        self.add_link(network,'n1','s6')
        self.add_link(network,'n1','s4')
        self.add_link(network,'s1','s2')
        self.add_link(network,'s2','s3')
        self.add_link(network,'s3','n2')

        self.add_link(network, 's4', 'n1')
        self.add_link(network, 's4', 's5')
        self.add_link(network, 's5', 's3')

        self.add_link(network, 's6', 'n1')
        self.add_link(network, 's6', 's7')
        self.add_link(network, 's7', 's8')
        self.add_link(network, 's8', 'n2')

        bandwidth = {}

        bandwidth['s1'] = 6000
        bandwidth['s2'] = 4000
        bandwidth['s3'] = 4000
        bandwidth['s4'] = 2000
        bandwidth['s5'] = 3000
        bandwidth['s6'] = 4000
        bandwidth['s7'] = 4000
        bandwidth['s8'] = 4000

        delay = {}

        delay['n1'] = {}
        delay['s1'] = {}
        delay['s2'] = {}
        delay['s3'] = {}
        delay['s4'] = {}
        delay['s5'] = {}
        delay['s6'] = {}
        delay['s7'] = {}
        delay['s8'] = {}

        self.add_delay(delay,'n1','s1',2)
        self.add_delay(delay, 's1', 's2', 2)
        self.add_delay(delay, 's2', 's3', 2)
        self.add_delay(delay, 's3', 'n2', 2)

        self.add_delay(delay, 'n1', 's6', 3)
        self.add_delay(delay, 's6', 's7', 0.5)
        self.add_delay(delay, 's7', 's8', 0.5)
        self.add_delay(delay, 's8', 'n2', 0.5)

        self.add_delay(delay, 'n1', 's4', 0.5)
        self.add_delay(delay, 's4', 's5', 0.5)
        self.add_delay(delay, 's5', 's3', 0.5)




        paths = []
        path = ['n1', 's2', 's1','n2']
        paths.append(path)
        path = ['n1', 's2', 's1', 's3', 'n2']
        paths.append(path)
        path = ['n1', 's7', 's1', 's8', 'n2']
        paths.append(path)
        path = ['n1', 's4', 's2', 's6', 'n2']
        paths.append(path)
        path = ['n1', 's1', 's2', 's8', 'n2']
        paths.append(path)
        # path = ['n1', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 'n2']
        # paths.append(path)
        # path = ['n1', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 's8', 's9', 'n2']
        # paths.append(path)

        # path = ['n1', 's1', 's2', 's3', 's4', 'n2']

        parentPool = []

        for path in paths:
            parentPool.append(Chromosome(path,get_fitness(path,bandwidth,delay,network),0,1))

        parentPool.sort(cmp)

        for parent in parentPool:
            print "path is " + str(parent.genes) + " \n Fitness is : " + str(parent.fitness.isValidPath) + " " + str(parent.fitness.connectedNodes)+ " " + str(parent.fitness.bandwidth)

        # poolsize = 10

        poolsize = 10

        # strategy = 0 => random generation
        # strategy = 1 => mutation
        # strategy = 2 => crossover

        maxGen = 300

        gen = 1

        print "Generation " + str(0)

        pathsPool = []
        for parent in parentPool:
            display(parent)
            pathsPool.append(parent.genes)

        childPool = []
        while (gen<maxGen):

            childPool = []
            for parent in parentPool:
                i = random.randrange(1,3)
                if(i==1):
                    child = mutate(parent.genes,network)
                    if child not in pathsPool:
                        if not isrepetitivePath(child):
                            childPool.append(Chromosome(child,get_fitness(child,bandwidth,delay,network),1,gen))
                else:
                    x = random.randrange(0,len(parentPool))
                    y = random.randrange(0,len(parentPool))
                    while y==x:
                        y = random.randrange(0, len(parentPool))

                    paths = crossover(parentPool[x].genes,parentPool[y].genes)
                    for path in paths:
                        if path not in pathsPool:
                            if not isrepetitivePath(path):
                                childPool.append(Chromosome(path,get_fitness(path,bandwidth,delay,network),2,gen))


            parentPool.sort(cmp)
            childPool.sort(cmp)
            if len(parentPool) > 10:
                parentPool = parentPool[:10]
            if len(childPool) > 10:
                childPool = childPool[:10]

            parentPool = parentPool + childPool
            pathsPool = []
            for parent in parentPool:
                pathsPool.append(parent.genes)
            print "The length of present pool is " + str( len(parentPool) )

            parentPool.sort(cmp)
            print "Generation " + str(gen)

            for parent in parentPool:
                display(parent)
                if(parent.fitness.isValidPath):
                    print("Fitness value : "+str(calculateFitness(parent)) )

            gen = gen + 1


        # path = ['n1', 's1', 's2', 's3', 's4', 'n2']
        #
        # print("fitness is " + str( get_fitness(path,bandwidth,network).connectedNodes) )
        # print('path is ' + str(path))
        # print network
        #
        # print "Hello here "
        #
        # # paths = [path]
        # for path in paths:
        #     print path
        #     if is_valid_Path(path, network):
        #         print str(path) + "is a valid path"
        #
        # path = ['n1', 's1', 's2', 's3', 's4','n2']
        #
        # paths = [path]
        # for i in range(0,20):
        #     x = len(paths)
        #     for path in range(0,x):
        #         x = mutate(paths[path],network)
        #         if x not in paths:
        #             paths.append(x)
        #
        #     print "The valid paths are : "
        #     for path in paths:
        #         if is_valid_Path(path,network):
        #             print str(path) + " is a valid path"
        #
        # print "Hello here "
        # # for path in paths:
        # #     print paths
        # print("\n")
        # path1=['n1','s1','s2','s7','s8','n2']
        # path2=['n1','s9','s2','s3','s4','n2']
        #
        # crossover(path1,path2)

if __name__=='__main__':

    n1 = Network()
    n1.test_network()



