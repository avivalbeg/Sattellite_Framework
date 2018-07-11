### The world the satellites and messages live in


import numpy as np
import satellites
import message
global c

class World:

    def __init__(self,original_satellites =[],dt = .1,error_rate=.001):
        """

        :param original_satellites:
        :param dt:
        :param error_rate:
        """
        self.satellites = []
        for satellite in original_satellites:
            self.satellites.append(satellite)
        self.dt = dt
        self.error_rate = error_rate
        self.flying_messages = []

    def add_satellite(self,satellite):
        self.satellites.append(satellite)


    def take_time_step(self,*args):
        """

        :return:
        """
        for satellite in self.satellites:
            #print(satellite.outgoing_message_buffer)
            if satellite.outgoing_message_buffer:
                mess1 = satellite.outgoing_message_buffer[0]
                #print(mess1)
                satellite.outgoing_message_buffer = []
                self.add_message(mess1,satellite.location,satellite.power)


        for satellite in self.satellites:
            satellite.move(self.dt)
            satellite.time +=1
            #satellite.accelerate(self.dt)
            for mess in self.flying_messages:
                intensity_of_message,real_message = mess.propagate(satellite.location)
                #print(real_message)
                print('Intensity of the Message is: %f for %s'%(intensity_of_message,satellite.sensitivity))
                satellite.write_to_receive_buffer(real_message,intensity_of_message)
            if satellite.flash != None:
                satellite.run_prog(satellite,*args)
        self.flying_messages =[]
            #send the messages to each of the satellites

    def add_message(self,mess,start_location,start_intensity):
        """

        :param message:
        :param start_location:
        :param start_intensity:
        :return:
        """
        #print(type(self.flying_messages))
        self.flying_messages.append(message.Message(mess,start_location,start_intensity))



# if __name__ == '__main__':


