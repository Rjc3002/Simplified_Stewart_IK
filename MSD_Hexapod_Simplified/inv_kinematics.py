from math import sqrt
import numpy as np
class inv_kinematics:
    def __init__(self,radious_base, radious_platform, gamma_base, gamma_platform, advanced=False, height=0.1, 
                 actuator_min=0, actuator_nominal=0, actuator_max=0) -> None:
        self.rb = radious_base  # radious of the base
        self.rp = radious_platform  # radious of the platform
        self.gamma_B = np.deg2rad(gamma_base)  # half of the angle of the base
        self.gamma_P = np.deg2rad(gamma_platform)  # half of the angle of the platform
        self.aNom = actuator_nominal
        self.aMin = actuator_min
        self.aMax = actuator_max
        self.height = height
        self.advanced = advanced
        
        self.B = None
        self.P = None
        self.L = None
        
    def frame(self):
        # Allocate for variables
        pi = np.pi

        ## Define the Geometry of the Base
        # phi_B (Polar coordinates)
        phi_B = np.array([ 
            7*pi/6 + self.gamma_B, 
            7*pi/6 - self.gamma_B,
            pi/2 + self.gamma_B, 
            pi/2 - self.gamma_B, 
            11*pi/6 + self.gamma_B, 
            11*pi/6 - self.gamma_B  
            ])


        # phi_P (Polar coordinates)
        # Direction of the points where the rod is attached to the platform.
        phi_P = np.array([
            3*pi/2 - self.gamma_P ,
            5*pi/6 + self.gamma_P,
            5*pi/6 - self.gamma_P,
            pi/6 + self.gamma_P, 
            pi/6 - self.gamma_P,
            3*pi/2 + self.gamma_P, 
            ])

        # Coordinate of the points where servo arms 
        # are attached to the corresponding servo axis.
        B = self.rb * np.array( [ 
            [ np.cos(phi_B[0]), np.sin(phi_B[0]), 0],
            [ np.cos(phi_B[1]), np.sin(phi_B[1]), 0],
            [ np.cos(phi_B[2]), np.sin(phi_B[2]), 0],
            [ np.cos(phi_B[3]), np.sin(phi_B[3]), 0],
            [ np.cos(phi_B[4]), np.sin(phi_B[4]), 0],
            [ np.cos(phi_B[5]), np.sin(phi_B[5]), 0] ])
        Bx = B[0][0]
        By = B[0][1]
        B = np.transpose(B)
            
        # Coordinates of the points where the rods 
        # are attached to the platform.
        P = self.rp * np.array([ 
            [ np.cos(phi_P[0]),  np.sin(phi_P[0]), 0],
            [ np.cos(phi_P[1]),  np.sin(phi_P[1]), 0],
            [ np.cos(phi_P[2]),  np.sin(phi_P[2]), 0],
            [ np.cos(phi_P[3]),  np.sin(phi_P[3]), 0],
            [ np.cos(phi_P[4]),  np.sin(phi_P[4]), 0],
            [ np.cos(phi_P[5]),  np.sin(phi_P[5]), 0] ])
        Px = P[0][0]
        Py = P[0][1]
        P = np.transpose(P)

        try:
            H = sqrt((self.aNom)**2 - ((Px-Bx)**2 + (Py-By)**2)) #Calculate height of the platform
        except ValueError:
            H = -1
        except Exception as e:
            print(f"Unexpected error: {e}")
        
        return B,P,H

    # Rotation matrices for X, Y, Z axis
    def rotX(self, theta):
        theta = np.deg2rad(theta)
        rotx = np.array([
            [1,     0    ,    0    ],
            [0,  np.cos(theta), -np.sin(theta)],
            [0,  np.sin(theta), np.cos(theta)] ])
        return rotx

    def rotY(self, theta): 
        theta = np.deg2rad(theta)   
        roty = np.array([
            [np.cos(theta), 0,  np.sin(theta) ],
            [0         , 1,     0       ],
            [-np.sin(theta), 0,  np.cos(theta) ] ])   
        return roty
        
    def rotZ(self, theta):  
        theta = np.deg2rad(theta)  
        rotz = np.array([
            [ np.cos(theta),-np.sin(theta), 0 ],
            [ np.sin(theta), np.cos(theta), 0 ],
            [   0        ,     0      , 1 ] ])   
        return rotz
    
    def solve(self, trans, rotation, searching=False):
        # Allocate for variables
        l = np.zeros((3,6))
        lll = np.zeros((6))
        # Calculate the coordinate point of base and platform
        self.B, self.P, self.H = self.frame()

        if(self.advanced):
            if not searching:
                print("Calculated neutral height (m): ",self.H)
            self.height = self.H

        if(self.height == -1):
            if not searching:
                print("Height calculation failed, please check the actuator lengths")
            return False

        self.home_pos= np.array([0, 0, self.height])         # home position of the platform, z-axis offset = perpendicular height

        # Get rotation matrix of platform. RotZ* RotY * RotX -> matmul
        # R = np.matmul( np.matmul(self.rotZ(rotation[2]), self.rotY(rotation[1])), self.rotX(rotation[0]) )
        R = np.matmul( np.matmul(self.rotX(rotation[0]), self.rotY(rotation[1])), self.rotZ(rotation[2]) )

        # Get leg length for each leg
        # leg = np.repeat(trans[:, np.newaxis], 6, axis=1) + np.repeat(home_pos[:, np.newaxis], 6, axis=1) + np.matmul(np.transpose(R), P) - B 
        l = np.repeat(trans[:, np.newaxis], 6, axis=1) + np.repeat(self.home_pos[:, np.newaxis], 6, axis=1) + np.matmul(R, self.P) - self.B 
        lll = np.linalg.norm(l, axis=0)

        minl = np.min(lll)
        maxl = np.max(lll)

        if(minl < self.aMin or maxl > self.aMax):
            if searching:
                return False
            else:
                print("Out of bounds!")

        # Position of leg in global frame
        self.L = l + self.B
        new_list = [(i, L) for i, L in enumerate(lll)]
        #print("leg lengths",new_list)
        if searching:
            return True
        return lll