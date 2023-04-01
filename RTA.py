from RSAfunctions import *
import socket
import pickle
import sys
import os

class RTA:
    vehiclesInfo = {}
    rsuInfo = {}

    def generateVehicleKeys(self, Vid):
        (publicKey, privateKey) = rsa.newkeys(1024)
        RTA.vehiclesInfo[Vid] = [publicKey,privateKey]
        return RTA.vehiclesInfo[Vid]

    def generateRsuKeys(self, Rid):
        (publicKey, privateKey) = rsa.newkeys(1024)
        RTA.rsuInfo[Rid] = [publicKey,privateKey]
        return RTA.rsuInfo[Rid]

    def sendMessage(self, port, message, option):
        s = socket.socket()
        s.connect(('localhost', port))

        # print(message, '\n')

        temp = [option, message]
        temp = pickle.dumps(temp)

        s.send(temp)
    
    def receiveMessage(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = 5000
        s.bind(('0.0.0.0', port))
        s.listen(3)
        addr = 0
        while True:
            if(addr == 0):
                c, addr = s.accept()
                data = (c.recv(4096))

            if(addr != 0):
                break
        
        data = pickle.loads(data)
        if(data[0] == "getPKv"):
            return self.vehiclesInfo[data[1]][0]

#-------------------


def read_file():
    with open("vehicleList.csv", "r") as f:
        SMRF1 = f.readlines()
    return SMRF1

initial = read_file()

while(True):
    
    current = read_file()
    if initial == current:
        continue

    initial = current

    # step 0 : initializing objects
    print("step 0: begins")
    print("--------------")

    print("Initializing...")
    rta = RTA()
    rsuKeys =  rta.generateRsuKeys('1000')
    vehicleKeys =  rta.generateVehicleKeys("4765")
    
    checker = 1
    while (checker == 1):
        try:
            rta.sendMessage(4765, vehicleKeys, 'keys')
            checker = 0
        except ConnectionRefusedError:
            print("connecting...")


    print("Initialization done")

    print("step 0: ends\n")

    # step 1 : RTA -> RSU
    print("step 1: begins")
    print("--------------")

    rta.sendMessage(1000, rsuKeys, 'keys')
    print("RTA -> RSU: keys sent")

    print("step 1: ends\n")

    # step 2 : RSU -> *


    # step 4 : Vechile -> RSU
    PKv = rta.receiveMessage()
    rta.sendMessage(1000, PKv, "VehPKv")

    # step 5 : verification of vehicle


    # step 6 : POI table distribution

    print("ended")

