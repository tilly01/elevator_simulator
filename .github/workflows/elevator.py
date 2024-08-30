import pygame
import time
class Elevator:
    def __init__(self, x, y, margin_top, margin_bottom):
        self.x_position = x
        self.y_position = y
        self.margin_top = margin_top
        self.margin_bottom = margin_bottom
        self.width = 80
        self.target_floor = None
        self.target_floors_up = []  # Ziel-Etagen beim Hochfahren
        self.target_floors_down = []  # Ziel-Etagen beim Herunterfahren
        self.current_target_list = 'up'
        self.current_target_index = 0
        self.speed = 5  # Geschwindigkeit des Aufzugs
        self.arrival_time = 0  # Zeitstempel, wann der Aufzug ankommt
        self.hold_time = 1  # Zeit, die der Aufzug auf jeder Etage anhalten soll (in Sekunden)
        self.holding = False
        self.passengers = []

    def set_target_floors(self, floors):
        """Setze die Ziel-Etagen für Auf- und Abfahrt."""
        self.target_floors_up = [i for i in range(len(floors))]
        self.target_floors_down = list(reversed(self.target_floors_up))
        self.current_target_list = 'up'
        self.current_target_index = 0
        if self.target_floors_up:
            self.set_target_floor(self.target_floors_up[self.current_target_index])

    def set_target_floor(self, target_floor):
        """Setze das Ziel für den Aufzug und initialisiere die Anhaltzeit."""
        self.target_floor = target_floor
        self.holding = False
        self.arrival_time = time.time()  # Zeitstempel bei der Ankunft

    def update_position(self, floor_positions, framerate):
        """Aktualisiere die Position des Aufzugs."""
        if self.target_floor is None:
            return

        target_y = floor_positions[self.target_floor]

        # Bewege den Aufzug zur Ziel-Position
        if self.y_position < target_y:
            self.y_position = min(self.y_position + self.speed, target_y)
        elif self.y_position > target_y:
            self.y_position = max(self.y_position - self.speed, target_y)

        # Überprüfe, ob der Aufzug die Ziel-Position erreicht hat
        if self.y_position == target_y:
            if not self.holding:
                self.holding = True
                self.arrival_time = time.time()  # Setze die Ankunftszeit
            if time.time() - self.arrival_time >= self.hold_time:
                # Wechsel die Richtung, wenn wir das Ende der Liste erreicht haben
                if self.current_target_list == 'up':
                    if self.current_target_index >= len(self.target_floors_up) - 1:
                        self.current_target_list = 'down'
                        self.current_target_index = 0
                    else:
                        self.current_target_index += 1
                elif self.current_target_list == 'down':
                    if self.current_target_index >= len(self.target_floors_down) - 1:
                        self.current_target_list = 'up'
                        self.current_target_index = 0
                    else:
                        self.current_target_index += 1

                # Setze die nächste Ziel-Etage
                if self.current_target_list == 'up':
                    self.set_target_floor(self.target_floors_up[self.current_target_index])
                elif self.current_target_list == 'down':
                    self.set_target_floor(self.target_floors_down[self.current_target_index])

    def draw(self, screen, fill_color, border_color):
        """Zeichne den Aufzug auf dem Bildschirm."""
        # Zeichne den Aufzug als ein Rechteck
        pygame.draw.rect(screen, fill_color, (self.x_position, self.y_position - 80, self.width, 80))
        pygame.draw.rect(screen, border_color, (self.x_position, self.y_position - 80, self.width, 80), 2)

        #vertikale mittel-linie
        middle_x = self.x_position + self.width // 2
        pygame.draw.line(screen, (255, 0, 0), (middle_x, self.y_position - 80), (middle_x, self.y_position), 2)
