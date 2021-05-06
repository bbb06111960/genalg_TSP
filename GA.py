#Team
# Raymond Madden
# Le Duong
# Erick Garcia Vargas
# All of us are using the hw policy for this assignment.
#Implemented Genetic Algorithm
import sys
import math
from math import sqrt
from random import randint, uniform

class city:
    def __init__(self, location=""):
        temp = location.split(" ")
        self.index = int(temp[0])-1
        self.fileindex = self.index+1
        self.x = float(temp[1])
        self.y = float(temp[2].strip("\n"))
        self.zero = round(sqrt((self.x**2)+(self.y**2)))
        self.prob = 0

def sort_population(population):  # sort population according to the distance
    sorted_population = population.copy()
    sorted_population.sort(key=lambda X:(X.zero, X.x, X.y, X.index))
    repeats(sorted_population)
    sorted_index = []
    for i in range(len(sorted_population)):
        if not(sorted_population[i].x == math.inf):
            sorted_index.append(sorted_population[i].index)
    return sorted_index

# in theory done
def euclideanDistance(city1, city2):
    d = sqrt(((city1.x - city2.x) ** 2) + ((city1.y - city2.y) ** 2))
    d = round(d)
    return d

def parseCityIndex(filename): #COMPLETE
    try:
        with open(filename, "r") as f:
            flines = f.readlines()

        x = True
        index = 0

        while x:
            if(flines[index]=="NODE_COORD_SECTION\n"):
                flines.pop(0)
                x = False
            else:
                index += 1

        for j in range(index):
            flines.pop(0)
        flines.pop()
        citylist = []

        for i in range (len(flines)):
            index = city(flines[i])
            citylist.append(index)

        return citylist
    except:
        return "Error"

def orderredo(population, dist):
    ord = []
    distancelist = dist.copy()
    i = round(uniform(0, len(distancelist) - 1))
    firstindex = distancelist[i]
    currentclose = math.inf
    currentcloseindex = 0
    Fulldistance = 0
    c = 0
    k = round(uniform(0, 0.5) * 100)
    while len(distancelist) > 1:
        for j in range(1, round(len(dist) / 4) + 2):
            if i == -1:
                i += len(distancelist)
            same = round(uniform(0, 1) * 100)
            try:
                if (not (i - j < 0)):
                    if ((same >= k) or currentclose == math.inf):
                        g = euclideanDistance(population[distancelist[i - j]], population[distancelist[i]])
                        if g < currentclose:
                            c = g
                            currentclose = g
                            currentcloseindex = i - j
            except:
                pass
            try:
                if ((same >= k) or currentclose == math.inf):
                    g = euclideanDistance(population[distancelist[i]], population[distancelist[i + j]])
                    if g < currentclose:
                        c = g
                        currentclose = g
                        currentcloseindex = i + j
                    else:
                        if (currentclose == math.inf):
                            g = euclideanDistance(population[distancelist[i]], population[distancelist[i + j]])
                            if g < currentclose:
                                c = g
                                currentclose = g
                                currentcloseindex = i + j
            except:
                pass
        Fulldistance += c
        ord.append([population[distancelist[i]], population[distancelist[currentcloseindex]]])
        if currentcloseindex < i:
            distancelist.pop(i)
            i = currentcloseindex

        if currentcloseindex > i:
            distancelist.pop(i)
            i = currentcloseindex - 1

        currentclose = math.inf
    ord.append([population[distancelist[0]], population[firstindex]])
    Fulldistance += euclideanDistance(population[distancelist[0]], population[firstindex])
    return ord, Fulldistance

def order(population, dist):
    ord = []
    distancelist = dist.copy()
    i = round(uniform(0, len(distancelist) - 1))
    firstindex = distancelist[i]
    currentclose = math.inf
    currentcloseindex = 0
    Fulldistance = 0
    c = 0
    k = round(uniform(0,0.5)*100)
    while len(distancelist) > 1:
        for j in range(1, round(len(dist) / 4) + 3):
            if i == -1:
                i += len(distancelist)
            same = round(uniform(0,1)*100)
            try:
                if (not (i - j < 0)):
                    if((same >= k) or currentclose == math.inf):
                        g = euclideanDistance(population[distancelist[i - j]], population[distancelist[i]])
                        if g < currentclose:
                            c = g
                            currentclose = g
                            currentcloseindex = i - j
            except:
                pass
            try:
                if((same >= k) or currentclose == math.inf):
                    g = euclideanDistance(population[distancelist[i]], population[distancelist[i + j]])
                    if g < currentclose:
                        c = g
                        currentclose = g
                        currentcloseindex = i + j
                    else:
                        if(currentclose == math.inf):
                            g = euclideanDistance(population[distancelist[i]], population[distancelist[i + j]])
                            if g < currentclose:
                                c = g
                                currentclose = g
                                currentcloseindex = i + j
            except:
                pass
        Fulldistance += c
        ord.append([population[distancelist[i]], population[distancelist[currentcloseindex]]])
        if currentcloseindex < i:
            distancelist.pop(i)
            i = currentcloseindex

        if currentcloseindex > i:
            distancelist.pop(i)
            i = currentcloseindex - 1

        currentclose = math.inf
    ord.append([population[distancelist[0]], population[firstindex]])
    Fulldistance += euclideanDistance(population[distancelist[0]], population[firstindex])
    return ord, Fulldistance

def findbest(population, distancelist):
    check = 0
    y = True
    current = math.inf
    currentlist = []
    default = 2
    if(len(distancelist)<100000):
        default = 5
    if (len(distancelist) < 10000):
        default = 10
    if (len(distancelist) < 1000):
        default = 50
    if (len(distancelist) < 100):
        default = 100
    if (len(distancelist) < 10):
        default = 500
    while(y):
        one, two = orderredo(population, distancelist)
        if(two < current):
            current = two
            currentlist = one
            check = 0
        if(two > current):
            check += 1
        if(check >= default):
            y = False
    return currentlist, current

def repeats(population):
    for i in range(len(population)):
        if i > 0 and i < len(population)-1:
            if population[i].x == population[i-1].x and population[i].y == population[i-1].y:
                population[i].x = math.inf
                population[i].y = math.inf
            if population[i].x == population[i + 1].x and population[i].y == population[i + 1].y:
                population[i].x = math.inf
                population[i].y = math.inf

def main():

    citys = parseCityIndex(sys.argv[1])

    if citys == "Error":
        print(citys)
    else:
        g = sort_population(citys)
        a, b = findbest(citys, g)
        print(b)
        for i in a:
            print(i[0].fileindex)

if __name__ == "__main__":
    main()
            
