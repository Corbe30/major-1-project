from RSAfunctions import *
import numpy as np
import csv
from communication_terminal import Communication_ternimal
from RSAfunctions import *
import socket
import pickle
import sys

print(csv.__version__)

class Mobility(object):
    """
    Mobility class defines the dynamics of single vehicles in the net.
    It is worth pointing out that this model simply considers one-dimensional 
    vehicle mobility scenarios.
    """
    def __init__(self,
                 v0 = 30.0, # desired speed in m/s
                 T = 1.5, # safe time headway in s
                 a = 1.0, # maximum acceleration in m/s^2
                 b = 3.0, # desired deceleration in m/s^2
                 delta = 4.0, # acceleration exponent
                 s0 = 2, # minimum distance in m
                 l0 = 5.0): # the length of each vehicle in m
        
        self.v0 = v0
        self.T = T
        self.a = a
        self.b = b
        self.delta = delta
        self.s0 = s0
        self.l0 = l0
        
    def car_following_IDM(self, front_vehicle, rear_vehicle):
        """
        Adopt the Intelligent Driver Model (IDM) for car following dynamics.
        """
        if isinstance(front_vehicle, Vehicle) and isinstance(rear_vehicle, Vehicle):
            
            x1 = front_vehicle.position[0]
            x2 = rear_vehicle.position[0]
            v1 = front_vehicle.speed[0]
            v2 = rear_vehicle.speed[0]
            
            net_distance = np.abs(x1-x2) - self.l0
            
            if rear_vehicle.direct_flag == 1:
                dv = v2 - v1     
                s = self.s0 + v2*self.T + (v2*dv)/(2*np.sqrt(self.a*self.b)) 
                component1 = (v2/self.v0)**self.delta
                component2 = (s/net_distance)**2
                rear_vehicle.acceleration[0] = self.a*(1.0 - component1 -component2)
            else:
                v1 = np.abs(v1)
                v2 = np.abs(v2)
                dv = v2 - v1 
                s = self.s0 + v2*self.T + (v2*dv)/(2*np.sqrt(self.a*self.b)) 
                component1 = (v2/self.v0)**self.delta
                component2 = (s/net_distance)**2
                rear_vehicle.acceleration[0] = (-1.0)*(self.a*(1.0 - component1 -component2))            
        else:
            rear_vehicle.acceleration[0] = 0.0

class Vehicle(object):
    """
    Vehicle class:
    the attributes consists of ID, direct_flag, lane_ID, 
     position array([x, y]), and some kinematics parameters
     including speed array([vx, vy]) and acceleration array([ax, ay]).
    """
    def __init__(self,
                 ID=0, # ID of the vehicle, an integer
                 direct_flag = 1, # an integer indicates the moving direction
                 lane_ID = 0, # an integer indicates the lane number
                 position = np.array([0.0,0.0]), # position vecotr in m
                 speed = np.array([0.0,0.0]), # speed vector in m/s
                 acceleration = np.array([0.0,0.0])): # acceleration in m/s^2
        
        self.ID = ID
        self.direct_flag = direct_flag
        self.lane_ID = lane_ID
        self.position = position
        self.speed = speed
        self.acceleration = acceleration

    Vid = ''
    vehicleKeys = [0]*2 #[public key, private key]
    RidPool = ['1000']
    POItable = []
    RsuPubKey = ''

    def sendMessage(self, port, message, option):
        s = socket.socket()
        s.connect(('localhost', port))

        temp = [option, message]
        temp = pickle.dumps(temp)

        s.send(temp)

    def receiveMessage(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = self.Vid
        s.bind(('0.0.0.0', int(port)))
        s.listen(3)
        addr = 0
        while True:
            if(addr == 0):
                c, addr = s.accept()
                data = (c.recv(4096))

            if(addr != 0):
                break

        data = pickle.loads(data)
        # print(data)

        if(data[0] == 'keys'):
            self.vehicleKeys = data[1]
        
        if(data[0] == 'RSUdetails'):
            self.RsuPubKey = data[1][2]
            # print('\n\n\n', "the rsupubkey is ", data, '\n\n')
            if(RSAverify(data[1][0], data[1][1], data[1][2])):
                print("Step 2: RSA verified")
            else:
                print("Step 2: RSA verification failed")

    def setup_communication_terminal(self, issource = False):
        self.communication_terminal = Communication_ternimal(self.ID, issource)
    
    def update_acceleration(self, mobility, front_vehicle = None):
            mobility.car_following_IDM(front_vehicle, self)
    
    def update_speed(self, dt):
        self.speed = self.speed + dt*self.acceleration
        
    def update_position(self, dt):
        self.position = self.position + self.speed*dt
