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
        r_P,r_B, gama_P,gama_B,height = self.design_variable
        self.clf = ik(r_P,r_B,gama_P,gama_B,height)
        # compute the leg length for the initial position
        translation = np.array([0, 0, 0])       # translation in meters
        rotation = np.array([0, 0, 0])         # rotation in degrees
        self.l  = self.clf.solve(translation, rotation)
        print("initial leg length (m) ",self.l)
        return 
        
    def start_simmulation(self, data):
        print("Starting Simulation")
        self.init_stewart()  # initialize the stewart platform
        for i in data:
            trans,rot = i
            l = self.clf.solve(trans, rot) # compute the leg length
            dl = l-self.l                  # compute the leg actuation distance (total_length - initial_length)
            print("Leg actuation distance (m) ",dl)
        return