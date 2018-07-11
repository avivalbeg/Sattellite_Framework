### The world the satellites live in


import numpy as np
from .satellites import *
from .message import Message
global c

class World:

    def __init__(self,original_satellites =[],dt = .05,error_rate=.001):
        """

        :param original_satellites:
        :param dt:
        :param error_rate:
        """
        c = 3e8
        self.satellites = []
        for satellite in original_satellites:
            self.satellites.append(satellite)
        self.dt = dt
        self.error_rate = error_rate
        self.flying_messages = []

    def add_satellite(self,satellite):
        self.satellites.append(satellite)


    def take_time_step(self):
        """

        :return:
        """
        for satellite in self.satellites:
            satellite.move(self.dt)
            satellite.time +=1
            #satellite.accelerate(self.dt)
            for message in self.flying_messages:
                intensity_of_message,real_message = message.propagate(satellite.location)
                if intensity_of_message>= satellite.sensitivity:
                    satellite.incoming_message_buffer.append(real_message)
        self.flying_messages =[]
            #send the messages to each of the satellites

    def add_message(self,message,start_location,start_intensity):
        """

        :param message:
        :param start_location:
        :param start_intensity:
        :return:
        """
        self.flying_messages.append(Message(message,start_location,start_intensity))



# if __name__ == '__main__':


