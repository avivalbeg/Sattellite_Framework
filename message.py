from numpy.linalg import norm
c = 3e8

global c

class Message:

    def __init__(self,message,start_location,initial_intensity,initial_radius=1):
        """

        :param message:
        :param start_location:
        :param initial_intensity:
        :param initial_radius:
        """
        self.message = message
        self.start_location =start_location
        self.start_intensity = initial_intensity
        self.start_radius = initial_radius
    def propagate(self,x2):
        """

        :param x1:
        :param x2:
        :return:
        """
        radius = norm(self.start_location-x2)
        intensity = self.start_intensity* (radius)/(self.start_radius)  # This is for the 2D geometry
        #intensity = self.start_intensity* (radius**2)/(self.start_radius**2) # This is for the 3D geometry
        return intensity



