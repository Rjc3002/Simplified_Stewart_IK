# Description: This file is used to test the stewart platform
import time
import os 
from inv_kinematics import inv_kinematics as ik
import numpy as np

class StewartPlatform:
    def __init__(self, design_variable) -> None:
        self.design_variable = design_variable

    def cls(self):
        os.system('cls')
        
    def init_stewart(self):
        # Design variables
        r_B,r_P,gama_B,gama_P,advanced,height,aMin,aNom,aMax = self.design_variable
        self.clf = ik(r_B,r_P,gama_B,gama_P,advanced,height,aMin,aNom,aMax)
        # compute the leg length for the initial position
        translation = np.array([0, 0, 0])       # translation in meters
        rotation = np.array([0, 0, 0])         # rotation in degrees
        self.l  = self.clf.solve(translation, rotation)
        print("initial leg length (m): ",self.l)
        return 
        
    def search_simulation(self,trans,rot):
        print("Starting search")
        results = np.zeros((3000,4))

        rvalues = np.arange(0.18, 0, -0.01)   #Search space for the radius (m)
        gvalues = np.arange(60, 0, -10)       #Search space for the gamma (deg)

        k=0
        found = False
        r_B,r_P,gama_B,gama_P,advanced,height,aMin,aNom,aMax = self.design_variable
        for r1 in rvalues:
            for r2 in rvalues:
                for g1 in gvalues:
                    for g2 in gvalues:
                        self.clf = ik(r1,r2,g1/2.0,g2/2.0,True,height,aMin,aNom,aMax)
                        if self.clf.solve(trans, rot, True): # compute the leg length
                            results[k] = (r1,r2,g1,g2)
                            k = k + 1
                            found = True
        if found:
            print("Search Results: ")
            print("   rB    rp    gB     gP   ")
            for i in range(k):
                formatted_array = np.array2string(results[i], formatter={'float_kind': lambda x: "%.3f" % x})
                print(formatted_array)
            return True
        return False


    def start_simmulation(self, data, searching=False):
        print("Starting Simulation")
        self.init_stewart()  # initialize the stewart platform
        for i in data:
            test = False
            trans,rot = i

            if searching:
                test = self.search_simulation(trans,rot)

            if test is False and searching:
                print("Search Failed...")
                return
            elif test and searching:
                print("Search Successful")

            l = self.clf.solve(trans, rot) # compute the leg length

            dl = l-self.l                  # compute the leg actuation distance (total_length - initial_length)
            print("Leg actuation distance (m): ",dl)
        return