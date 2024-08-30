import pygame
class Person:
    def __init__(self, floor_y_position, target_floor=None, image=None):
        self.width = 30
        self.height = 30
        self.color = (0, 255, 0)
        self.x_position = 0  # Startposition am linken Rand des Bildschirms
        self.y_position = floor_y_position - self.height // 2  # Vertikale Position auf der Etage
        self.target_floor = target_floor if target_floor is not None else 0  # Standard-Zielgeschoss ist 0
        self.in_elevator = False  # Ob die Person im Aufzug ist oder nicht
        self.speed = 1  # Bewegungsgeschwindigkeit der Person
        self.image = image  # Das Bild der Person
        self.visible = True  # Sichtbarkeit der Person
        self.rect = pygame.Rect(self.x_position, self.y_position, self.width, self.height)

    def draw(self, screen):
        if self.visible:
            if self.image:
                screen.blit(self.image, (self.x_position, self.y_position))
            else:
                pygame.draw.rect(screen, self.color, self.rect)

    def move_towards_elevator(self, elevator):
        if not self.in_elevator and self.visible:
            if self.x_position < elevator.x_position:
                self.x_position += self.speed
                self.rect.x = self.x_position

    def update_position(self, elevator):
        if self.in_elevator:
            self.y_position = elevator.y_position + (elevator.height // 2) - (self.height // 2)
            self.rect.y = self.y_position

    def enter_elevator(self, elevator):
        if not self.in_elevator and self.rect.colliderect(elevator.rect):
            self.in_elevator = True
            self.visible = False  # Person wird unsichtbar, wenn sie in den Aufzug einsteigt
            elevator.passengers.append(self)

    def exit_elevator(self, elevator):
        if self.in_elevator and self.target_floor == elevator.current_floor:
            self.in_elevator = False
            self.x_position = elevator.x_position + elevator.width  # Bewege die Person aus dem Aufzug heraus
            elevator.passengers.remove(self)
            self.visible = True  # Person wird wieder sichtbar, wenn sie aus dem Aufzug aussteigt
