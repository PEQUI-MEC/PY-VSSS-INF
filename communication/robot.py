class Robot:
    def __init__(self):
        """
        Robot Constructor

        Creates a vector with robot's addresses.
        Addresses will be used to connect with robots
        Args:

        Returns:
        """
        self.robots = {
            "C": "\x56\x0D",
            "F": "\x6B\x0D",
            "G": "\x21\x5C"
        }
