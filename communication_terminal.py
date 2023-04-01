class Communication_ternimal(object):
    def __init__(self,
                 ID, # terminal ID
                 received_flag = False): # flag indicating whether receiving a message
        self.ID = ID
        self.received_flag = received_flag
        self.buffer_max_length = 100
        self.message_buffer = []
        
    def receive(self,message):        
        if len(self.message_buffer) < self.buffer_max_length:
            self.message_buffer.append(message)
            
        if self.message_buffer:
            self.received_flag = True
        else:
            self.received_flag = False
    
    def update_buffer(self):
        # more complicated buffering protocol should be done in future
        pass
    
    def send(self,neighboring_node):
        for message in self.message_buffer:
            neighboring_node.communication_terminal.receive(message)


