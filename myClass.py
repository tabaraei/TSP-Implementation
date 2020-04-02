import math
import random

class City:         # Models a city
   def __init__(self, x=None, y=None):           # constructs a city
      self.x = None
      self.y = None
      if x is not None:
         self.x = x
      else:
         self.x = int(random.random() * 200)
      if y is not None:
         self.y = y
      else:
         self.y = int(random.random() * 200)

   def getX(self):          # Gets city's x coordinate
      return self.x

   def getY(self):          # Gets city's y coordinate
      return self.y

   def distanceTo(self, city):          # Gets the distance to given city
      xDistance = abs(self.getX() - city.getX())
      yDistance = abs(self.getY() - city.getY())
      distance = math.sqrt((xDistance*xDistance) + (yDistance*yDistance))
      return distance

   def __repr__(self):
      return str(self.getX()) + ", " + str(self.getY())


class TourManager:          # Holds the cities of a tour
   destinationCities = []           # Holds our cities

   def addCity(self, city):         # Adds a destination city
      self.destinationCities.append(city)

   def getCity(self, index):        # Get a city
      return self.destinationCities[index]

   def numberOfCities(self):        #  Get the number of destination cities
      return len(self.destinationCities)


class Tour:              # Stores a candidate tour
   def __init__(self, tourmanager, tour=None):
      self.tourmanager = tourmanager
      self.tour = []             # Holds our tour of cities
      self.fitness = 0.0            # Cache
      self.distance = 0             # Cache
      if tour is not None:
         self.tour = tour
      else:
         for i in range(0, self.tourmanager.numberOfCities()):              # Constructs a blank tour
            self.tour.append(None)

   def __len__(self):
      return len(self.tour)

   def __getitem__(self, index):
      return self.tour[index]

   def __setitem__(self, key, value):
      self.tour[key] = value

   def __repr__(self):
      geneString = "";
      for i in range(0, self.tourSize()):
         geneString += "(" + str(self.getCity(i)) + ")" + " --> "
      geneString += "(" + str(self.getCity(0)) + ")"
      return geneString

   def generateIndividual(self):               # Creates a random individual
      for cityIndex in range(0, self.tourmanager.numberOfCities()):             # Loop through all our destination cities and add them to our tour
         self.setCity(cityIndex, self.tourmanager.getCity(cityIndex))
      random.shuffle(self.tour)             # Randomly reorder the tour

   def getCity(self, tourPosition):         # Gets a city from the tour
      return self.tour[tourPosition]

   def setCity(self, tourPosition, city):           # Sets a city in a certain position within a tour
      self.tour[tourPosition] = city
      self.fitness = 0.0            # If the tours been altered we need to reset the fitness and distance
      self.distance = 0

   def getFitness(self):        # Gets the tours fitness
      if self.fitness == 0:
         self.fitness = 1/float(self.getDistance())
      return self.fitness

   def getDistance(self):           # Gets the total distance of the tour
      if self.distance == 0:
         tourDistance = 0
         for cityIndex in range(0, self.tourSize()):        # Loop through our tour's cities
            fromCity = self.getCity(cityIndex)          # Get city we're travelling from
            destinationCity = None              # City we're travelling to
            if cityIndex+1 < self.tourSize():           # Check we're not on our tour's last city, if we are set our tour's final destination city to our starting city
               destinationCity = self.getCity(cityIndex+1)
            else:
               destinationCity = self.getCity(0)
            tourDistance += fromCity.distanceTo(destinationCity)            # Get the distance between the two cities
         self.distance = tourDistance
      return self.distance

   def tourSize(self):          # Get number of cities on our tour
      return len(self.tour)

   def containsCity(self, city):            # Check if the tour contains a city
      return city in self.tour


class Population:           # Manages a population of candidate tours
   def __init__(self, tourmanager, populationSize, initialise):
      self.tours = []           # Holds population of tours
      for i in range(0, populationSize):        # Construct a population
         self.tours.append(None)

      if initialise:            # If we need to initialise a population of tours do so
         for i in range(0, populationSize):         # Loop and create individuals
            newTour = Tour(tourmanager)
            newTour.generateIndividual()
            self.saveTour(i, newTour)

   def __setitem__(self, key, value):
      self.tours[key] = value

   def __getitem__(self, index):
      return self.tours[index]

   def saveTour(self, index, tour):         # Saves a tour
      self.tours[index] = tour

   def getTour(self, index):            # Gets a tour from population
      return self.tours[index]

   def getFittest(self):          # Gets the best tour in the population
      fittest = self.tours[0]
      for i in range(0, self.populationSize()):         # Loop through individuals to find fittest
         if fittest.getFitness() <= self.getTour(i).getFitness():
            fittest = self.getTour(i)
      return fittest

   def populationSize(self):            # Gets population size
      return len(self.tours)


class GA:           # Manages algorithms for evolving population
   def __init__(self, tourmanager):         # Initialize GA parameters
      self.tourmanager = tourmanager
      self.mutationRate = 0.015
      self.tournamentSize = 5
      self.elitism = True

   def evolvePopulation(self, pop):             # Evolves a population over one generation
      newPopulation = Population(self.tourmanager, pop.populationSize(), False)
      elitismOffset = 0         # Keep our best individual if elitism is enabled
      if self.elitism:
         newPopulation.saveTour(0, pop.getFittest())
         elitismOffset = 1

      # Crossover population
      for i in range(elitismOffset, newPopulation.populationSize()):             # Loop over the new population's size and
         parent1 = self.tournamentSelection(pop)          # Select parents       # create individuals from Current population
         parent2 = self.tournamentSelection(pop)          # Select parents
         child = self.crossover(parent1, parent2)         # Crossover parents
         newPopulation.saveTour(i, child)                 # Add child to new population

      for i in range(elitismOffset, newPopulation.populationSize()):        # Mutate the new population a bit to add some new genetic material
         self.mutate(newPopulation.getTour(i))

      return newPopulation

   def crossover(self, parent1, parent2):           # Applies crossover to a set of parents and creates offspring
      child = Tour(self.tourmanager)        # Create new child tour

      startPos = int(random.random() * parent1.tourSize())          # Get start and end sub tour positions for parent1's tour
      endPos = int(random.random() * parent1.tourSize())

      for i in range(0, child.tourSize()):          # Loop and add the sub tour from parent1 to our child
         if startPos < endPos and i > startPos and i < endPos:          # If our start position is less than the end position
            child.setCity(i, parent1.getCity(i))
         elif startPos > endPos:        # If our start position is larger
            if not (i < startPos and i > endPos):
               child.setCity(i, parent1.getCity(i))

      for i in range(0, parent2.tourSize()):        # Loop through parent2's city tour
         if not child.containsCity(parent2.getCity(i)):         # If child doesn't have the city add it
            for ii in range(0, child.tourSize()):           # Loop to find a spare position in the child's tour
               if child.getCity(ii) == None:            # Spare position found, add city
                  child.setCity(ii, parent2.getCity(i))
                  break

      return child

   def mutate(self, tour):          # Mutate a tour using swap mutation
      for tourPos1 in range(0, tour.tourSize()):        # Loop through tour cities
         if random.random() < self.mutationRate:        # Apply mutation rate
            tourPos2 = int(tour.tourSize() * random.random())       # Get a second random position in the tour

            city1 = tour.getCity(tourPos1)          # Get the cities at target position in tour
            city2 = tour.getCity(tourPos2)
            # Swap them around
            tour.setCity(tourPos2, city1)
            tour.setCity(tourPos1, city2)

   def tournamentSelection(self, pop):          # Selects candidate tour for crossover
      tournament = Population(self.tourmanager, self.tournamentSize, False)         # Create a tournament population
      for i in range(0, self.tournamentSize):        # For each place in the tournament get a random candidate tour and add it
         randomId = int(random.random() * pop.populationSize())
         tournament.saveTour(i, pop.getTour(randomId))
      fittest = tournament.getFittest()         # Get the fittest tour
      return fittest
