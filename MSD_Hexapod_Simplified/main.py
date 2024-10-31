#!/usr/bin/env python3

# Based on: https://github.com/mlayek21/Stewart-Platform/tree/main

# Ryland Charron
# rjc3002
# 10/30/2024

from StewartPlatform import StewartPlatform as sp
import MSD_Hexapod_Simplified
import numpy as np

"""
3DOF Stewart Platform RPR configuration analysis:
    - We take 6Dof Stewart Platform as a reference.
    - We fix the platform in the home position.
    - The platfrom can only rotate in the x,y,z axis roll, pitch yaw.
"""

# Set Hexapod Constants
design_variables = [MSD_Hexapod_Simplified.RB, MSD_Hexapod_Simplified.RP, MSD_Hexapod_Simplified.GB, 
                    MSD_Hexapod_Simplified.GP,MSD_Hexapod_Simplified.AdvancedMode, MSD_Hexapod_Simplified.H, 
                    MSD_Hexapod_Simplified.Actuator_Min, MSD_Hexapod_Simplified.Actuator_Neutral, MSD_Hexapod_Simplified.Actuator_Max]

# Create translation
trans = np.array([MSD_Hexapod_Simplified.dX, MSD_Hexapod_Simplified.dY, MSD_Hexapod_Simplified.dZ]) 

# Create Rotation
rot1 = np.array([MSD_Hexapod_Simplified.dRoll, MSD_Hexapod_Simplified.dPitch, MSD_Hexapod_Simplified.dYaw]) 


# Define the desired end effector position
data = [[trans, rot1]]

# Create the stewart platform object
clf = sp(design_variables)

if __name__ == '__main__':
        clf.start_simmulation(data,MSD_Hexapod_Simplified.SearchMode) # Calculate Actuator lengths
        
