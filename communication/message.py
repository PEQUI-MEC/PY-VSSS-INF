class Message:
    def __init__(self, robotId, message):
        """
        Message Constructor

        Construtor que cria uma mensagem, constituída do id do robô
        e da mensagem a ser enviada

        Args:
            robotId (int): Robot id
            message (string): message to send
         Returns:
        """
        self.robotId = robotId
        self.message = message
