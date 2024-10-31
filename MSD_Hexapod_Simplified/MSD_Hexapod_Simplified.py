# Header file for easy control of variables

# Define the stewart platform design variables
RP, RB = 0.08, 0.08         # meters, radius of platform and base
GP, GB = 30/2, 30/2       # degrees, polar angle between adjacent mounting points for platform and base. 
                          # Pairs of mounts are evenly spaced on a triangle
H = 0.1                   # meters, height of the platform (z-axis) relative to base



# Define the operation to perform
#   Linear Translation of Platform (meters)
dX = 0;
dY = 0;
dZ = 0;

#   Rotation of Platform (degrees)
dRoll = 10;
dPitch = 10;
dYaw = 0; # Twist