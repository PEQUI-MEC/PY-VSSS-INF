class Robot():
    def __init__(self):
		"""Robot Constructor
			
			Creates a vector with robot's addresses.
			Addresses will be used to connect with robots
	        Args:
	        
	        Returns:

	    """
		self.robots = []
		self.robots.append("\x56\x0D")
		self.robots.append("\x6B\x0D")
		self.robots.append("\x21\x5C")