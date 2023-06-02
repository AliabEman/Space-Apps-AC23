# README: This is just a demo for our PyGame project, 
# TODO: 
# 1- we need to change the reference entity (the SUN) to the Earth
# 2- we will need to change the existing objects & list into a list that can read the NASA Data.
# 3- we need to reference Dylan's calculations in order to get an idea of the trajectory we plan to display



# Article containing inspiration for planet values: https://fiftyexamples.readthedocs.io/en/latest/gravity.html
import math
import pygame

#Set up pygame window
WIDTH, HEIGHT = 800, 800
#Set up the PYGAME window we draw onto, pass the WIDTH and HEIGHT as a TUPLE
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Planet Simulation")

#rgb's for our pywindow
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
WHITE = (250, 250, 250)

FONT = pygame.font.SysFont("comicsans", 16)

# Implementing the planets:
class Planet:
    # Constants to use in the simulation

    # Astronomical Unit, approx equal to the distance from the Earth to the Sun:
    # 1 AU = 149.6e6 * 1000 m from the sun
    AU = (149.6e6 * 1000)
    # Gravitational Constant, used in finding the force of attraction in objects:
    G = 6.67428e-11
    # Scale, if our planet is moving at x km/s, we cant draw that speed, we need to scale it appropriately.
    # We need to find what 1 m represents in px.
    SCALE = 250 / AU # Here we will say, 1 AU = approx 100 px
    # How much time do we want to represent as being elapsed in our simulation, TIMESTEP
    TIMESTEP = 3600* 24 # Representing one day at a time updating the planet.


    
    # Define the initialization of the planets, with their dimensions for the game
    def __init__(self, x, y, radius, color, mass):
        # Position of planet on the screen in m
        self.x = x 
        self.y = y
        self.radius = radius
        
        self.color = color
        # Mass in kg of the planet, used to calculate the attraction between planets for circular orbit
        self.mass = mass
        
        # Used to keep track of all the points this planet has travelled on, so we can draw a circular orbit representing
        # the orbit of the planet
        self.orbit = []

        # planet of orbit (in our case will be Earth, in this situation, its the sun)
        # We do not want to have the orbit for the Sun, we want to draw the orbit for the planets surrounding the Sun
        self.sun = False
        # To know the distance from the sun, we have this relative position in order to keep distance
        # We update this for every planet that we have, relative to our planet to orbit
        self.distance_to_sun = 0 
        # Velocity for the movement of the planets in the game.
        # We can generate a circle by having the x,y velocities moving at a constant speed,
        # makes a circular design, in m
        self.x_vel = 0
        self.y_vel = 0

    # We need to draw the planet
    def draw(self, win):
        # bring the values to scale
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2

        # Get a list of updated points (scaled to the screen)
        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                # Update and append the new x,y
                updated_points.append((x,y))
            # Take a list of points and draw them w/o enclosing them
            pygame.draw.lines(WIN, self.color, False, updated_points, 2)
        # draw the circle on the window (win), with the color, position (x,y) and radius
        pygame.draw.circle(win, self.color, (x,y), self.radius)

        # Create the text object to get the distance at any given point
        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE)
            WIN.blit(distance_text, (x - distance_text.get_width()/2,y - distance_text.get_height()/2))

    # Method to calculate the force of attraction between another object
    # and the current object
    def attraction(self, other):
        other_x, other_y = other.x, other.y
        # calculate the distance between the two objects
        distance_x = other_x - self.x
        distance_y = other_y - self.y

        distance = math.sqrt(distance_x **2 + distance_y ** 2)

        if other.sun:
            # If the object being calculated for the distance from the sun
            # IS the sun, we calculate the distance to the sun
            self.distance_to_sun = distance

        # Calculate the force of attraction
        force = self.G * self.mass * other.mass / distance**2

        # this method, math.atan2 can find the angle for theta between
        # y and x distance
        theta = math.atan2(distance_y, distance_x)

        # Force components
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
        
    # method to update the position according to the current
    # and other planet
    def update_position(self, planets):
        # Get the total forces exerted on the current planet that are not
        # the current planet
        total_fx = total_fy = 0
        for planet in planets:
            # we arent looking to calculate the force between the current
            # planet and the current planet
            if self == planet:
                continue
            # calculate the force exerted on the current planet
            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy
        # Calculate the velocity
        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        # Update the x, y position using the velocity and timestamp
        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        # Append the x and y position to draw the orbit 
        # around the current planet.
        self.orbit.append((self.x, self.y))

# Set the Pygame Event Loop, an infinite loop which runs the entire time the simulation is going 
# (essential to games in order to keep track of the changes happening)

def main():
    run = True
    # A clock is implemented to synchronize our game to our liking, not the resources of the computers
    # We are choosing to run at the speed of our variable, not the computers processor here.
    # We regulate the framerate this way within the run loop.
    clock = pygame.time.Clock()

    sun = Planet(0,0, 30, YELLOW, 1.98892 * 10 ** 30) # mass in kg
    # We dont draw the distance to sun from sun, and orbit from sun, recall sun boolean
    sun.sun = True
    
    earth = Planet(-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24)
    earth.y_vel = 29.783 *1000

    mars = Planet(-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10 **23)
    mars.y_vel = 24.077 * 1000

    mercury = Planet(0.387 * Planet.AU, 0, 8, DARK_GREY, 0.330 * 10**24)
    mercury.y_vel = -47.4 * 1000

    venus = Planet(0.723 * Planet.AU, 0, 14, WHITE, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000
    
    # Create a list of planets
    planets = [sun, earth, mars, mercury, venus]


    # Infinite loop to keep program running instead of instantly closing
    while run:
        # we allow our game to run our clock at a maximum of 60 frames per second.
        clock.tick(60)
        # We need to refresh the screen, in order to see in stop-motion
        WIN.fill((0,0,0))

        # Get the different events occuring in the pygame
        # Key presses, mouse clicks, etc
        # The more advanced the game, the more events that get handled
        for event in pygame.event.get():
            # We handle if the event window is exited w/ the x button in the window.
            if event.type == pygame.QUIT:
                run = False
            # To display a drawing action (multipart):
            # 1- We want to draw something onto the screen
            #WIN.fill(WHITE)
            # 2- Takes all of the drawing actions done since the last update, pastes them and draws
            # them onto the screen
        # Call the planets list to draw onto the display
        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()
