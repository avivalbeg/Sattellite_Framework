#The Satellites themselves

# Right now there is no control

import numpy as np
from .message_helpers import make_swap_message,convert_to_binary
global c

class Satellite:


    def __init__(self,satellite_name,original_state,network,sensitivity = 0,receive_buffer_size = 1000,role = 'drone',transmit_buffer_size =100, memory_size=320000, transmission_speed=32000,initiation_size=2,World = None):
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
        self.network_id = convert_to_binary(network,16)
        self.time = 0 # time.time()  ## All clocks start synchronized
        self.name = satellite_name   #if you want the satellites to take on different roles
        self.location = np.array(original_state[:dimension/2])
        self.velocity = np.array(original_state[dimension/2:])
        self.role = 'drone'
        self.recieve_buffer =np.array()
        self.transmit_buffer = np.array()
        self.memory = np.zeros(memory_size)
        self.preamble = '10101010'*initiation_size
        #self.world = World
        self.incoming_message_buffer = []

    # def add_message(self):
    #     self.world.make_message(self)
    #     #function, destination_sat, destination_reg, hop
    #     #message = make_swap_message(preamble=self.preamble,network_id=self.network_id,function=function,destination_sat=destination_sat,source_sat=self.name,destination_reg=destination_reg,hopo=hop)
    #     for satellite in self.world.satellites:
    #         distance = norm(self.location-np.array(satellite.location))

    def write_to_receive_buffer(self,transmission,location=0):
        """

        :param transmission:
        :param location:
        :return:
        """
        if transmission.intensity >= self.sensitivity:
            self.recieve_buffer[location:location+len(transmission)] = transmission.message

    def write_to_transmission_buffer(self,location,message):
        """

        :param location:
        :param message:
        :return:
        """
        self.transmit_buffer[location:location+len(message)] = message

    def clear_transmission_buffer(self):
        """

        :return:
        """
        self.transmit_buffer =np.array()

    def clear_recieve_buffer(self):
        """

        :return:
        """
        self.recieve_buffer = np.array()

    def write_to_memory(self,location,message):
        """

        :param location:
        :param message:
        :return:
        """
        self.memory[location:location+len(message)] = message


if __name__ == '__main__':
    print(make_swap_message())



