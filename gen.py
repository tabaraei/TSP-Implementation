import math
import random
from myClass import *

if __name__ == '__main__':          # Create a tour and evolve a solution

   tourmanager = TourManager()

   # Create and add our cities
   city1 = City(14, 96)
   tourmanager.addCity(city1)
   city2 = City(31, 93)
   tourmanager.addCity(city2)
   city3 = City(61, 45)
   tourmanager.addCity(city3)
   city4 = City(16, 18)
   tourmanager.addCity(city4)
   city5 = City(33, 68)
   tourmanager.addCity(city5)
   city6 = City(3, 2)
   tourmanager.addCity(city6)
   city7 = City(50, 96)
   tourmanager.addCity(city7)
   city8 = City(95, 58)
   tourmanager.addCity(city8)
   city9 = City(12, 20)
   tourmanager.addCity(city9)
   city10 = City(53, 38)
   tourmanager.addCity(city10)
   city11 = City(89, 71)
   tourmanager.addCity(city11)
   city12 = City(56, 34)
   tourmanager.addCity(city12)
   city13 = City(70, 7)
   tourmanager.addCity(city13)
   city14 = City(31, 57)
   tourmanager.addCity(city14)
   city15 = City(72, 32)
   tourmanager.addCity(city15)
   city16 = City(33, 45)
   tourmanager.addCity(city16)
   city17 = City(54, 16)
   tourmanager.addCity(city17)
   city18 = City(20, 68)
   tourmanager.addCity(city18)
   city19 = City(80, 26)
   tourmanager.addCity(city19)
   city20 = City(80, 28)
   tourmanager.addCity(city20)

   # Initialize population
   pop = Population(tourmanager, 50, True)
   initDis = str(pop.getFittest().getDistance())


   # Evolve population for 100 generations
   ga = GA(tourmanager)
   pop = ga.evolvePopulation(pop)
   for i in range(0, 100):
      pop = ga.evolvePopulation(pop)

   # Print final results
   print ("\nTSP:")
   print (pop.getFittest())
   print ("\n------------------------------------------------------------")
   print ("Initial distance: " + initDis)
   print ("Final distance: " + str(pop.getFittest().getDistance()))
