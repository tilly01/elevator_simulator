import pygame
from person import Person

class Floor:
    def __init__(self, floor_number, y_position):
        self.floor_number = floor_number
        self.y_position = y_position
        self.passenger_image = pygame.image.load("images/passenger.png")
        self.passenger_image = pygame.transform.scale(self.passenger_image, (20, 30))  # Größe anpassen, falls nötig
        self.passengers = []  # Liste für Passagiere

    def draw(self, screen, font, margin_left, floor_height):
        # Zeichne Stockwerk-Beschriftung
        text = font.render(self.get_floor_label(), True, (0, 0, 0))
        text_rect = text.get_rect(midleft=(margin_left - 30, self.y_position - floor_height // 1.4))
        screen.blit(text, text_rect)

        # Zeichne Passagiere
        for i, passenger in enumerate(self.passengers):
            passenger_x_position = margin_left - 120 + i * (self.passenger_image.get_width())
            screen.blit(self.passenger_image, (passenger_x_position, self.y_position - floor_height // 4.4))

    def get_floor_label(self):
        # Bestimme die richtige Bezeichnung für das Stockwerk
        if self.floor_number == 0:
            return "UG"
        elif self.floor_number == 1:
            return "EG"
        else:
            return str(self.floor_number - 1)

    def spawn_passenger(self):
        # Füge einen neuen Passagier hinzu
        self.passengers.append("Passenger")
    def spawn_passenger(self, image=None):
        # Nutze das übergebene Bild oder das Standard-Passagierbild
        image_to_use = image if image else self.passenger_image
        new_passenger = Person(self.y_position, image=image_to_use)  # Optionales Argument für Bild hinzufügen
        self.passengers.append(new_passenger)

