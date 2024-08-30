import pygame
import random
from os.path import abspath, dirname, join
from elevator import Elevator  # Importiere die Elevator-Klasse
from floor import Floor  # Importiere die Floor-Klasse
from person import Person

# arrow
BASE_PATH = abspath(dirname(__file__))
IMAGE_PATH = join(BASE_PATH, 'images')
IMG_NAMES = ['arrow_down', 'arrow_up', 'passenger', 'stairs']

# Farben
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
gray = (200, 200, 200)

# Pygame initialisieren
pygame.init()
screen = pygame.display.set_mode([1200, 600])
pygame.display.set_caption('ELEVATOR')
framerate = 60
timer = pygame.time.Clock()
clock = pygame.time.Clock()
background = white

font = pygame.font.Font(None, 30)

# Treppen-Bild laden und skalieren
stairs_img = pygame.image.load(join(IMAGE_PATH, 'stairs.png'))
stairs_img = pygame.transform.scale(stairs_img, (25, 25))
person_image = pygame.image.load(join(IMAGE_PATH, 'passenger.png'))


class TextBox:
    def __init__(self, x, y, w, h, font):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = gray
        self.text = ''
        self.font = font
        self.txt_surface = self.font.render(self.text, True, black)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
            else:
                self.active = False
            self.color = black if self.active else gray

        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_RETURN:
                    self.text = ''
                elif event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                self.txt_surface = self.font.render(self.text, True, black)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


def initialize_floors(num_floors, margin_top, margin_bottom):
    floor_height = (margin_bottom - margin_top) // num_floors
    floors = []
    for i in range(num_floors):
        y_position = margin_bottom - i * floor_height
        floors.append(Floor(i, y_position))
    return floors


def draw_start_screen(textboxes):
    screen.fill(white)
    font = pygame.font.Font(None, 74)
    text = font.render("ELEVATOR SIMULATION", True, black)
    text_rect = text.get_rect(center=(600, 80))
    screen.blit(text, text_rect)

    font = pygame.font.Font(None, 25)
    labels = ["Elevators", "Floors", "Time"]
    positions = [(100, 160), (100, 200), (100, 240)]

    for i, (label, pos) in enumerate(zip(labels, positions)):
        text = font.render(label, True, black)
        text_rect = text.get_rect(center=pos)
        screen.blit(text, text_rect)
        textboxes[i].draw(screen)

    start_button = pygame.Rect(500, 350, 200, 50)
    pygame.draw.rect(screen, black, start_button)
    start_text = font.render("Start", True, white)
    start_text_rect = start_text.get_rect(center=start_button.center)
    screen.blit(start_text, start_text_rect)

    pygame.display.flip()
    return start_button


def draw_simulation_elements(elevators, floors, num_elevators):
    screen.fill(background)

    # Ränder (fest)
    margin_left = 150
    margin_right = 1150
    margin_top = 60
    margin_bottom = 560

    # Berechne die Höhe der einzelnen Etagen
    floor_height = (margin_bottom - margin_top) // len(floors)

    # Zeichne die Randlinien (oben, unten, links, rechts)
    pygame.draw.line(screen, black, (margin_left, margin_top), (margin_right, margin_top), 1)
    pygame.draw.line(screen, black, (margin_left, margin_bottom), (margin_right, margin_bottom), 1)
    pygame.draw.line(screen, black, (margin_left, margin_top), (margin_left, margin_bottom), 1)
    pygame.draw.line(screen, black, (margin_right, margin_top), (margin_right, margin_bottom), 1)

    # Zeichne horizontale Linien für Floors
    for floor in floors:
        pygame.draw.line(screen, black, (margin_left, floor.y_position), (margin_right, floor.y_position), 1)
        # Übergabe von margin_left und floor_height an floor.draw
        floor.draw(screen, font, margin_left, floor_height)

        # Treppen-Bild zeichnen
        stairs_rect = stairs_img.get_rect()
        stairs_rect.midleft = (margin_left - 140, floor.y_position - 60)
        screen.blit(stairs_img, stairs_rect)

    # Zeichne vertikale Linien für Aufzüge
    column_widths = []
    for i in range(len(elevators)):
        if i % 2 == 0:  # Vergrößere jede zweite Spalte
            column_widths.append(int(1.5 * (margin_right - margin_left) // (len(elevators) + 1)))
        else:
            column_widths.append((margin_right - margin_left) // (len(elevators) + 1))

    total_width = sum(column_widths)
    start_x = margin_left + (margin_right - margin_left - total_width) // 2

    # Zeichne die vertikalen Linien für Aufzugsschächte und die Aufzüge
    current_x = start_x

    # Aufzüge aktualisieren und zeichnen
    for i, elevator in enumerate(elevators):
        elevator_width = column_widths[i]
        elevator.x_position = current_x
        elevator.width = elevator_width
        elevator.update_position([floor.y_position for floor in floors], framerate)
        elevator.draw(screen, white, red)  # Weiß mit rotem Rand
        # Vertikaler roter Strich in der Mitte des Aufzugs
        pygame.draw.line(screen, black, (current_x, margin_top), (current_x, margin_bottom), 1)
        pygame.draw.line(screen, black, (current_x + elevator_width, margin_top), (current_x + elevator_width, margin_bottom), 1)
        pygame.draw.line(screen, black, (current_x + elevator_width, margin_top),
                         (current_x + elevator_width, margin_bottom), 1)
        current_x += elevator_width

    pygame.display.flip()

def main():
    textboxes = [
        TextBox(220, 140, 140, 32, font),
        TextBox(220, 180, 140, 32, font),
        TextBox(220, 220, 140, 32, font)
    ]

    running = True
    simulation_started = False
    num_elevators, num_floors = 3, 5
    margin_top = 60
    margin_bottom = 560
    floors = initialize_floors(num_floors, margin_top, margin_bottom)
    # Initialisiere den Passagier-Spawn-Timer
    passenger_timer = pygame.time.get_ticks()
    spawn_interval = 3000  # Spawning-Intervall in Millisekunden (1 Sekunde)

    while running:
        timer.tick(framerate)
        clock.tick(framerate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            for box in textboxes:
                box.handle_event(event)

        if not simulation_started:
            start_button = draw_start_screen(textboxes)
            if pygame.mouse.get_pressed()[0]:
                if start_button.collidepoint(pygame.mouse.get_pos()):
                    try:
                        num_elevators = int(textboxes[0].text) if textboxes[0].text.isdigit() else 3
                        num_floors = int(textboxes[1].text) if textboxes[1].text.isdigit() else 5
                        num_time = int(textboxes[2].text) if textboxes[2].text.isdigit() else 30

                        floors = initialize_floors(num_floors, margin_top, margin_bottom)
                        elevators = [
                            Elevator(0, floors[-1].y_position, margin_top, margin_bottom) for _ in range(num_elevators)
                        ]

                        # Setze die Ziel-Etagen für jeden Aufzug
                        for elevator in elevators:
                            elevator.set_target_floors([i for i in range(len(floors))])
                            floor_height = (margin_bottom - margin_top) // num_floors
                            elevator.height = floor_height // 1.2
                        for i, elevator in enumerate(elevators):
                            if i % 2 == 0:  # Große Aufzüge
                                elevator.speed = 1.0
                            else:  # Kleine Aufzüge
                                elevator.speed = 2.0
                            elevator.height = floor_height // 1.2  # Aufzugshöhe setzen
                            if i % 2 == 0:
                                elevator.speed = 1.0  # Große Aufzüge
                            else:
                                elevator.speed = 2.0  # Kleine Aufzüge

                        simulation_started = True
                    except ValueError:
                        print("Please enter valid numbers in all fields.")
        else:
            # Zeitsteuerung für Passagier-Spawn
            current_time = pygame.time.get_ticks()
            if current_time - passenger_timer > spawn_interval:
                random_floor = floors[random.randint(0, num_floors - 1)]
                random_floor.spawn_passenger()
                passenger_timer = current_time
                random_floor = floors[random.randint(0, len(floors) - 1)]
                random_floor.spawn_passenger(person_image)  # Passagier wird mit benutzerdefiniertem Bild gespawnt
                passenger_timer = current_time  # Timer zurücksetzen

            draw_simulation_elements(elevators, floors, num_floors)
        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()



# in else: elevator set target for 0
