# passenger.py
class Passenger:
    def __init__(self, start_floor, destination_floor):
        self.start_floor = start_floor
        self.destination_floor = destination_floor
        self.image = None  # Platz für das Bild des Passagiers
        self.x_position = 0
        self.y_position = 0

    def draw(self, screen, font):
        # Hier könnten Sie den Passagier zeichnen, z.B. mit `self.image`
        pass
