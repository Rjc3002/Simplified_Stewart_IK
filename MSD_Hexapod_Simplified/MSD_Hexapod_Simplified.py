# Header file for easy control of variables

# Define the stewart platform design variables
#RP, RB = 0.08, 0.08         # meters, radius of platform and base
#GP, GB = 30/2, 30/2         # degrees, polar angle between adjacent mounting points for platform and base. 
                             # Pairs of mounts are evenly spaced on a triangle

H = 0.1                   # meters, height of the platform (z-axis) relative to base, unused when AdvancedMode=True

AdvancedMode=True         # If True, will perform calculations for the height of the platform based on the neutral length of the actuator
                          # And will check for out of bounds motions using the actuator limits

SearchMode=False           # If True, will perform a search for the useable configurations of the stewart platform given the actuator limits

# Define Linear Actuator Specifications, Unused when AdvancedMode=False
# For CLA2201 Without COE
# https://www.jpe-innovations.com/wp-content/uploads/CLA2201_Datasheet.pdf
Actuator_Min = 0.0376
Actuator_Neutral = 0.0436
Actuator_Max = 0.0496
RB, RP = 0.08, 0.04
GB, GP = 50/2, 50/2

# For CVCA1     -> Only passes search with small radii
# https://www.jpe-innovations.com/wp-content/uploads/CVCA1_Datasheet.pdf
#Actuator_Min = 0.0275
#Actuator_Neutral = 0.030
#Actuator_Max = 0.0335
#RB, RP = 0.04, 0.02
#GB, GP = 30/2, 30/2

# For Cryogenic Fine Positioning Linear Actuator        -> Requires a small platform radii to pass search
# https://www.moog.com/content/dam/moog/literature/sdg/space/spacecraft-mechanisms/moog-cryogenic-fine-positioning-linear-actuator-datasheet.pdf
#Actuator_Min = 0.16764
#Actuator_Neutral = 0.173355
#Actuator_Max = 0.17907
#RB, RP = 0.08, 0.02
#GB, GP = 30/2, 30/2



# Define the operation to perform
#   Linear Translation of Platform (meters)
dX = 0;
dY = 0;
dZ = 0;

#   Rotation of Platform (degrees)
dRoll = 10;
dPitch = 10;
dYaw = 0; # Twist