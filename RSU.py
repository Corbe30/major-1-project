from RSAfunctions import *
import socket
import pickle
import sys

class RSU:
    RSUid = ''
    T = ''
    PSv = ''
    SIGv = ''
    rsuKeys = [0]*2 #[public key, private key]

    def sendMessage(self, port, message, option):
        s = socket.socket()
        s.connect(('localhost', port))

        temp = [option, message]
        temp = pickle.dumps(temp)

        s.send(temp)

    def receiveMessage(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port = self.RSUid
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
        if(data[0] == 'keys'):
            self.rsuKeys = data[1]
        
        if(data[0] == 'joinRequest'):
            self.PSv = data[1][0]
            self.SIGv = data[1][1]

            Vid = RSAdecrypt(self.PSv, self.rsuKeys[1])
            # print("\n Vid is : ", Vid, "\n")
            return Vid

        if(data[0] == 'VehPKv'):
            PKv = data[1]
            return RSAverify(str(self.PSv), self.SIGv,PKv)




#-------------------

while(True):
    # step 0 : initializing objects
    rsu1 = RSU()
    rsu1.RSUid = 1000

    # step 1 : RTA -> RSU
    rsu1.receiveMessage()


    # step 2 & 3: RSU -> *
    print("step 2 & 3: begins")
    print("------------------")

    print("RSU -> *: broadcasting RSU details...")
    SIGr = RSAsign(str(rsu1.RSUid), rsu1.rsuKeys[1])


    rsu1.sendMessage(4765, [str(rsu1.RSUid), SIGr, rsu1.rsuKeys[0]], 'RSUdetails')
    print("RSU -> *: broadcasted")

    print("step 2 & 3: ends\n")

    # step 4 : Vechile -> RSU
    Vid = rsu1.receiveMessage()

    # step 5 : verification of vehicle
    print("step 5: begins")
    print("--------------")

    print("Verifying vehicle with RTA...")
    rsu1.sendMessage(5000, Vid, "getPKv")
    if(rsu1.receiveMessage()):
        print("vehicle verified")
    else:
        print("vehicle verification failed")
        blacklist.append(Vid)

    print("step 5: ends\n")
    # step 6 : POI table distribution

    print("ended")