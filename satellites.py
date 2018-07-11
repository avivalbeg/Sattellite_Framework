#The Satellites Themselves

# Right now there is no control

import numpy as np
global c

def convert_to_binary(number,size):
    """

    :param number:
    :param size:
    :return:
    """
    binary= ''
    if number == None:
        return binary
    for i in range(size,0,-1):
        number2 = number%(2**(i-1))
        if number2 == number:
            binary+='0'
        else:
            binary +='1'
        number = number2
    return binary


class Satellite:


    def __init__(self,original_state=[0,0,0,0,0,0],network=1,satellite_name = None,sensitivity = 1,power =10,receive_buffer_size = 1000,role = 'drone',transmit_buffer_size =100, memory_size=320000, transmission_speed=32000,initiation_size=2,World = None):
        """

        :param satellite_name:
        :param original_state:
        :param network:
        :param sensitivity:
        :param receive_buffer_size:
        :param role:
        :param transmit_buffer_size:
        :param memory_size:
        :param transmission_speed:
        :param initiation_size:
        """
        dimension = len(original_state)
        self.sensitivity =sensitivity
        self.power = power
        self.network_id = convert_to_binary(network,16)
        self.time = 0 # time.time()  ## All clocks start synchronized
        self.name = satellite_name   #if you want the satellites to take on different roles
        self.location = np.array(original_state[:int(dimension/2)])
        self.velocity = np.array(original_state[int(dimension/2):])
        self.role = 'drone'
        self.recieve_buffer =''
        self.transmit_buffer = ''
        self.memory = np.zeros(memory_size)
        self.preamble = '10101010'*initiation_size
        self.flash = None
        #self.world = World
        self.incoming_message_buffer = []
        self.outgoing_message_buffer = []

    # def add_message(self):
    #     self.world.make_message(self)
    #     #function, destination_sat, destination_reg, hop
    #     #message = make_swap_message(preamble=self.preamble,network_id=self.network_id,function=function,destination_sat=destination_sat,source_sat=self.name,destination_reg=destination_reg,hopo=hop)
    #     for satellite in self.world.satellites:
    #         distance = norm(self.location-np.array(satellite.location))

    def write_to_receive_buffer(self,message,intensity,location=0):
        """

        :param transmission:
        :param location:
        :return:
        """
        if intensity >= self.sensitivity:
            #print('yes')
            #self.recieve_buffer[location:location+len(transmission)] = transmission.message
            self.recieve_buffer += message

    def write_to_transmission_buffer(self,message,location=0):
        """

        :param location:
        :param message:
        :return:
        """
        #print(message)
        t = message
        #self.transmit_buffer[location:location+len(message)] = message
        self.transmit_buffer = message
        #print(self.transmit_buffer)
    def clear_transmission_buffer(self):
        """

        :return:
        """
        self.transmit_buffer =''

    def clear_recieve_buffer(self):
        """

        :return:
        """
        self.recieve_buffer = ''

    def write_to_memory(self,location,message):
        """

        :param location:
        :param message:
        :return:
        """
        self.memory[location:location+len(message)] = message

    def send_message(self):
        #print('sending...')
        self.outgoing_message_buffer.append(self.transmit_buffer)
        #print(self.transmit_buffer)
        self.clear_transmission_buffer()

    def move(self,dt):
        self.location = self.location + self.velocity*dt

    def flash_prog(self,prog):
        self.flash = prog

    def run_prog(self,*args):
        if self.flash == None:
            print('You need to flash a program')
        else:
            return self.flash(*args)

    def clear_flash(self):
        self.flash = None
        print('%s is unflashed'%self.name)


if __name__ == '__main__':
    def blah(a,b):
        return a+b
    A = Satellite()
    A.flash_prog(blah)
    print(A.run_prog(1,2))



