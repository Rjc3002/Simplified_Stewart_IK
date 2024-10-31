# Header file for easy control of variables

# Define the stewart platform design variables
RP, RB = 0.08, 0.08         # meters, radius of platform and base
GP, GB = 30/2, 30/2       # degrees, polar angle between adjacent mounting points for platform and base. 
                          # Pairs of mounts are evenly spaced on a triangle
H = 0.1                   # meters, height of the platform (z-axis) relative to base

                          # Can probably modify such that Height is calculated based on GP & GB
                          #    and the neutral length of a specific linear actuator, using
                          #    the right triangle of the mounting points projected down to get the hypotenuse
                          #    and then solve for H using that hypotenuse and the actuator length?
                          # Would also be easy to add constraints for min/max actuator stroke.



# Define the operation to perform
#   Linear Translation of Platform (meters)
dX = 0;
dY = 0;
dZ = 0;

#   Rotation of Platform (degrees)
dRoll = 10;
dPitch = 10;
dYaw = 0; # Twist