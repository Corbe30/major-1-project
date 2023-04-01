from RSAfunctions import *
import socket
import pickle
import sys

class Vehicle:
    Vid = ''
    vehicleKeys = [0]*2 #[public key, private key]
    RidPool = ['1000']
    POItable = []
    RsuPubKey = ''

    # def R2V(self,RSUid, SIGr, rsuPublicKeys):
    #     return RSAverify(RSUid, SIGr, rsuPublicKeys)

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

#-------------------

