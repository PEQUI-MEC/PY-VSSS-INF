class Velocity:
	"""Robot Constructor
		
		Initialize values with id = -1 and velocities equals 0

		Args:
        
        Returns:

    """
    def __init__(self):
        self.id = -1
        self.left_wheel = 0
        self.right_wheel= 0
    
    """Setup method
		
		Save Velocity values.

        Args:
        	id (int): robot value
			left_wheel (float): left wheel velocity
			right_wheel (float): right wheel velocity
        
        Returns:

    """
    def setup(self, id, left_wheel, right_wheel):
        self.id = id
        self.left_wheel = left_wheel
        self.right_wheel = right_wheel
