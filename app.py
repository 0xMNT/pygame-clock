import math
from datetime import datetime

import pygame

pygame.init()


# font and size
font_path = "JetBrainsMonoNLNerdFontMono-Regular.ttf"
font = pygame.font.Font(font_path, 30)  # None means default font, 74 is the font size


# pygame setup
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True


# Colors
background = "#101010"
green = "#40916c"
s_color = "#415a77"
m_color = "#778da9"
h_color = "#e0e1dd"


# Parameters
circle_radius = 30  # Radius of the antialiased circle
rotation_radius = 200  # Distance from the center to the circle's path
angle_speed = 1
center = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


# Helper Functions
def GetTime():
    now = datetime.now()
    hours = int(now.strftime("%I"))  # Hours (12-hour clock) without leading zero
    minutes = int(now.strftime("%M"))  # Minutes without leading zero
    seconds = int(now.strftime("%S"))  # Seconds without leading zero
    return now, hours, minutes, seconds


# save all x,y coordinates in a list for all points on a circle
def generate_circle_points(center, radius, num_points=360):
    points = []
    cx, cy = center

    for i in range(num_points):
        angle_deg = (360 / num_points) * i
        angle_rad = math.radians(angle_deg - 90)

        x = cx + radius * math.cos(angle_rad)
        y = cy + radius * math.sin(angle_rad)

        points.append((x, y))
    return points


screen.fill(background)

# lists with x,y coordinates of the circles
seconds_coordinates = generate_circle_points(center, 280)
minutes_coordinates = generate_circle_points(center, 200)
hours_coordinates = generate_circle_points(center, 120)

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:  # Check if the "Esc" key is pressed
                running = False

    # set variables for time
    now, h, m, s = GetTime()

    # fill screen with background color
    screen.fill(background)

    # draw circle from 0 to the current time in hours, minuts or seconds
    for i in seconds_coordinates[: s * 6]:
        pygame.draw.aacircle(screen, s_color, (i[0], i[1]), 30)
    for i in minutes_coordinates[: m * 6]:
        pygame.draw.aacircle(screen, m_color, (i[0], i[1]), 30)
    for i in hours_coordinates[: h * 30]:
        pygame.draw.aacircle(screen, h_color, (i[0], i[1]), 30)

    # Get the current time
    current_time = datetime.now()

    # Format seconds with leading zero for clock in the center of screen
    hours = current_time.strftime("%H")
    minutes = current_time.strftime("%M")
    seconds = current_time.strftime("%S")
    current_time = f"{hours}:{minutes}:{seconds}"

    # Render the current time as text
    time_text = font.render(current_time, True, "#eae0d5")

    # Get the rectangle of the text surface and position it
    text_rect = time_text.get_rect(center=(center[0], center[1]))

    # Draw the text on the screen
    screen.blit(time_text, text_rect)

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    dt = clock.tick(60) / 1000

pygame.quit()
