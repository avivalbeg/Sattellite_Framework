## To translate and produce messages

## This is where you can customize to your specific situation

## This is for the SWAP packet structure

import world
import satellites
import numpy as np

######################################################################################################################
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

#####################################################################################################################################
def convert_from_binary(binary):
    """

    :param binary:
    :return:
    """
    max_exponent = len(binary)
    out = 0
    for i in range(max_exponent):
        out+= (2**(i))*int(binary[max_exponent-i-1])
    return out



#####################################################################################################################################
def make_swap_message(preamble='10101010'*2, network_id=1, function=2, destination_sat=41, source_sat=32,
                      destination_reg=2, hop=1, thing='01110', source_reg=0):
    """

    :param preamble:
    :param network_id:
    :param function:
    :param destination_sat:
    :param source_sat:
    :param destination_reg:
    :param hop:
    :param thing:
    :param source_reg:
    :return:
    """
    if thing == None:
        thing = ''

    message = preamble

    # network id is 4 bytes long and it tells us what channel we are listening to and the source and destination satellite ids
    message += convert_to_binary(network_id, 4)

    message += convert_to_binary(source_sat, 8)

    message += convert_to_binary(destination_sat, 8)

    # The function code
    if function == 0:   #status(This is the requested value.)
        function = '1010'
    elif function == 1:  #query(What is the requested value?)
        function = '0101'
    elif function == 2:  #command(change the value at a register)
        function = '1111'

    message += function

    # The destination register is
    message += convert_to_binary(destination_reg, 8)

    # message += convert_to_binary(source_reg,8)

    message += convert_to_binary(hop, 4)

    message += thing

    message += convert_to_binary(len(message) + 16, 16)

    return message


###########################################################################################################################

def read_swap_message(message,preamble='10101010'*2):
    """

    :param message:
    :param preamble:
    :return:
    """

    important_part = message[16:]   #after preamble
    #print(important_part[:4])

    network_id = convert_from_binary(important_part[:4])
    #print(important_part[4:12])
    source_sat = convert_from_binary(important_part[4:12])
    destination_sat = convert_from_binary(important_part[12:20])
    func = important_part[20:24]
    # The function code
    if func == '1010':   #status(This is the requested value.)
        func = 0
    elif func == '0101':  #query(What is the requested value?)
        func = 1
    elif func == '1111':  #command(change the value at a register)
        func = 2
    dest_reg = important_part[24:32]
    hop = convert_from_binary(important_part[32:36])
    mess = important_part[36:-16]
    count = convert_from_binary(important_part[-16:])
    if count != len(message):
        print('There was a mistake. count: %d , actual: %d'%(count,len(message)))
    return([network_id,source_sat,destination_sat,func,dest_reg,hop,mess])


########################################################################################################################


if __name__ == '__main__':

    #Simple test world with two satellites
    #make the world
    Test_World = world.World()

    #making our first stationary satellite at the origin and adding it to the world
    s1 = satellites.Satellite(original_state=np.array([0,0,0,0,0,0]),network=1,satellite_name='1')
    Test_World.add_satellite(s1)

    #making our second stationary satellite at (0,0,1) and add it to the world
    s2 = satellites.Satellite(original_state=np.array([0, 0, 1, 0, 0, 0]), network=1,satellite_name='2')
    Test_World.add_satellite(s2)

    #making our first SWAP message. You can make any packet structure or behavior you like.
    sample = make_swap_message(preamble='10101010'*2, network_id=1, function=2, destination_sat=41, source_sat=32,
                      destination_reg=2, hop=1, thing='01110', source_reg=0)
    print("The SWAP message is %s"%sample)

    #We stage the message for transmission in the satellite
    s2.write_to_transmission_buffer(sample)

    #We then stage the message from satellite two in the world. When the message is sent from here the out_message_buffer will be cleared.
    print('sending from satellite 2')
    s2.send_message()

    #taking the time step moves the satellites forward in time dt
    Test_World.take_time_step()

    # We can then check if the first satellite received the message
    print(s1.recieve_buffer== sample)

    #Now we also made a SWAP decoder so we can see what it means

    print('network_id: %d, Source Satellite ID: %d, Destination Satellite ID: %d, function: %d, destination location: %s, hop: %d, message: %s, '%tuple(read_swap_message(s1.recieve_buffer)))

    #So now is the cool part! We can flash each satellite with a different program that we program in python and simulate how it'll behave.
    # In this way it is completely customizable and testable to different environments and
    #print(Test_World.satellites)



    #message = make_swap_message()
    #print(convert_to_binary(5,4))
    #args = read_swap_message(message)











