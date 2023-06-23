import pygame
import math
import sys

# Pygame initialization
pygame.init()
WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT), pygame.DOUBLEBUF)
pygame.display.set_caption("Planet Simulation")

class Planet(pygame.sprite.Sprite):
    def __init__(self, x, y, radius, color, speed):
        super().__init__()
        self.image = pygame.Surface((radius * 2, radius * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (radius, radius), radius)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.angle = 0
        self.laps_completed = 0
        self.distance_incremented = False

    def update(self, center_x, center_y):
        if self.speed != 0:  # Skip the update for the blue planet
            self.angle += self.speed

            # Update position based on the angle and laps completed
            if self.laps_completed < 3:
                if not self.distance_incremented:
                    radius = 150 + self.laps_completed * 50
                    self.rect.center = (
                        center_x + radius * math.cos(math.radians(self.angle)),
                        center_y + radius * math.sin(math.radians(self.angle))
                    )
                else:
                    radius = 200 + (self.laps_completed - 3) * 50
                    self.rect.center = (
                        center_x + radius * math.cos(math.radians(self.angle)),
                        center_y + radius * math.sin(math.radians(self.angle))
                    )
            else:
                radius = 200 + (3 - 1) * 50
                self.rect.center = (
                    center_x + radius * math.cos(math.radians(self.angle)),
                    center_y + radius * math.sin(math.radians(self.angle))
                )

    def draw(self, win):
        win.blit(self.image, self.rect)

def create_visualization_screen(selected_planet, efficiency_index, sec_mass):
    run = True
    clock = pygame.time.Clock()

    center_x = WIDTH // 2
    center_y = HEIGHT // 2

    font = pygame.font.Font(None, 28)

    # Load and resize the background image
    background_image = pygame.image.load("./images/galaxy.jpg")
    background_surface = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

    planets_group = pygame.sprite.Group()

    earth = Planet(center_x, center_y, 30, pygame.Color("blue"), 0)
    planets_group.add(earth)

    orbit_speed = 2  # Increase the orbit speed
    orbiting_planet = Planet(center_x + 150, center_y, 20, pygame.Color("green"), orbit_speed)
    planets_group.add(orbiting_planet)

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        orbiting_planet.update(center_x, center_y)

        WIN.blit(background_surface, (0, 0))  # Blit the background image onto the window

        # Draw orbit lines while orbiting
        for i in range(min(orbiting_planet.laps_completed + 1, 4)):
            radius = 150 + i * 50
            pygame.draw.circle(WIN, pygame.Color("white"), (center_x, center_y), radius, 1)

        planets_group.update(center_x, center_y)
        planets_group.draw(WIN)

        # Display planet information at the top of the screen
        info_text = f"Selected Planet: {selected_planet} | Efficiency: {efficiency_index} | Mass: {sec_mass}"
        info_surface = font.render(info_text, True, pygame.Color("white"))
        WIN.blit(info_surface, (10, 10))

        pygame.display.update()
        clock.tick(60)

        # Increment distance after completing three laps
        if orbiting_planet.laps_completed == 3:
            orbiting_planet.distance_incremented = True

        # Check if the planet completed a full lap
        if orbiting_planet.angle >= 360:
            orbiting_planet.angle = 0
            orbiting_planet.laps_completed += 1

    pygame.quit()

if __name__ == "__main__":
    selected_planet = sys.argv[1]
    efficiency_index = sys.argv[2]
    sec_mass = sys.argv[3]

    create_visualization_screen(selected_planet, efficiency_index, sec_mass)