import pygame
import math
pygame.init()

WIDTH, HEIGHT = 800, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulação dos Planetas by Sabrina M. Ferraz")

WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
BLUE = (100, 149, 237)
RED = (188, 39, 50)
DARK_GREY = (80, 78, 81)
BROWN = (139, 69, 19)

FONT = pygame.font.SysFont("arial", 16)

class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    SCALE = 250 / AU # 1AU = 100 pixels
    TIMESTEP = 3600*24 #1 dia

    def __init__(self, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass

        self.orbit = []
        self.sun = False
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def draw(self, WIN): #Desenho dos planetas
        x = self.x * self.SCALE + WIDTH / 2
        y = self.y * self.SCALE + HEIGHT / 2
        pygame.draw.circle(WIN, self.color, (int(x), int(y)), self.radius)

        if len(self.orbit) > 2:
            update_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.SCALE + WIDTH / 2
                y = y * self.SCALE + HEIGHT / 2
                update_points.append((x, y)) #Denhando as linhas

            pygame.draw.lines(WIN, self.color, False, update_points, 2)
            pygame.draw.circle(WIN, self.color, (x, y), self.radius)

        if not self.sun:
            distance_text = FONT.render(f"{round(self.distance_to_sun/1000, 1)}km", 1, WHITE) #Print em KM dos planetas
            WIN.blit(distance_text, (x, y))

    def attraction(self, other): #Cálculos da atração 
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y

        for point in self.orbit:
            x, y = point
            x = x * self.SCALE + WIDTH / 2
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance**2 #Cálculo do r
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y
    
    def update_position(self, planets):
        total_fx = total_fy = 0
        for other in planets:
            if self == other:
                continue

            fx, fy = self.attraction(other)
            total_fx += fx
            total_fy += fy


        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP #F = m / a a = f / m

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))
        


def main():
    run = True
    clock = pygame.time.Clock()
        
    sun = Planet(0, 0, 30, YELLOW, 1.988992 * 10**30)
    sun.sun = True

    earth = Planet (-1 * Planet.AU, 0, 16, BLUE, 5.9742 * 10**24) #eixo y para deixar ao redor do sol
    earth.y_vel = 29.783 * 1000

    mars = Planet (-1.524 * Planet.AU, 0, 12, RED, 6.39 * 10**23)
    mars.y_vel = 24.077 * 1000
        
    mercury = Planet (0.387 * Planet.AU, 0, 8, DARK_GREY, 3.30 * 10**23)
    mercury.y_vel = 47.4 * 1000

    venus = Planet (0.723 * Planet.AU, 0, 14, BROWN, 4.8685 * 10**24)
    venus.y_vel = -35.02 * 1000


    planets = [sun, earth, mars, mercury, venus]
    
    while run:
        clock.tick(60)
        WIN.fill((0, 0, 0))

        for event in pygame.event.get(): #Fechar a janela
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(WIN)

        pygame.display.update()

    pygame.quit()

main()