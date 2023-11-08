import pygame
import numpy as np

##### CONFIG #####
window_size = (1920, 1080)

#fps = 1000
fps = 60

force_fields_count = 50
force_fields_force = 0.01
random_ang_vel_change = 0.1
ang_vel_friction = 0.001

particles_count = 10000
particles_friction = 0.01
dir_force_limit = 0.005



show_force_fields = False

#base_size = 1
#size_speed_mul = 3

color1 = (255, 194, 28)
color2 = (96, 255, 64)

##################

and_vel_friction = 1 - ang_vel_friction

color1 = np.array(color1)
color2 = np.array(color2)

# pygame init
pygame.init()
window = pygame.display.set_mode(window_size)
clock = pygame.time.Clock()



map_width = window_size[0] / window_size[1]

rad360deg = 2 * np.pi

# x, y, rotation, angular velocity
force_fields = np.column_stack((
    np.random.uniform(0, map_width, force_fields_count),
    np.random.uniform(0, 1, force_fields_count),
    np.random.uniform(0, rad360deg, force_fields_count),
    np.zeros(force_fields_count)
))

# x, y, x vel, y vel, r, g, b
particles = np.column_stack((
    np.random.uniform(0, map_width, particles_count),
    np.random.uniform(0, 1, particles_count),
    np.zeros(particles_count),
    np.zeros(particles_count),
    np.zeros(particles_count, dtype=np.int8),
    np.zeros(particles_count, dtype=np.int8),
    np.zeros(particles_count, dtype=np.int8)
))


# repeat color
color1 = np.tile(color1, (particles_count, 1))
color2 = np.tile(color2, (particles_count, 1))

delta = 1 / fps

# main loop
while True:

    # update force fields
    force_fields[:, 3] += np.random.uniform(-random_ang_vel_change, random_ang_vel_change, force_fields_count)
    force_fields[:, 3] *= and_vel_friction

    force_fields[:, 2] += force_fields[:, 3] * delta

    force_fields[:, 2] %= rad360deg


    # update particles
    for ff in force_fields:
        dist = ((ff[0] - particles[:, 0]) ** 2 + (ff[1] - particles[:, 1]) ** 2) ** 0.5
        directional_force = force_fields_force / dist ** 2 * delta

        directional_force = np.where(directional_force > dir_force_limit, dir_force_limit, directional_force)

        particles[:, 2] += np.cos(ff[2]) * directional_force
        particles[:, 3] += np.sin(ff[2]) * directional_force

    particles[:, 0] += particles[:, 2] * delta
    particles[:, 1] += particles[:, 3] * delta

    # color
    speed = (particles[:, 2] ** 2 + particles[:, 3] ** 2) ** 0.5

    speed = np.maximum(1 - speed, 0)


    particles[:, 4:7] = color1 * speed.reshape((-1, 1)) + color2 * (1 - speed.reshape((-1, 1)))



    particles[:, 0] %= map_width
    particles[:, 1] %= 1

    particles[:, 2] *= 1 - particles_friction
    particles[:, 3] *= 1 - particles_friction






    # events, keypresses, mouse input etc.
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    window.fill((0, 0, 0))
    
    if show_force_fields:
        # draw force fields
        for ff in force_fields:
            pygame.draw.circle(
                window, 
                (200, 200, 255),
                (
                    int(ff[0] * window_size[1]), 
                    int(ff[1] * window_size[1])
                ), 
                5
            )

            # draw vector
            pygame.draw.line(
                window,
                (150, 150, 255),
                (
                    int(ff[0] * window_size[1]), 
                    int(ff[1] * window_size[1])
                ),
                (
                    int(ff[0] * window_size[1] + np.cos(ff[2]) * 100),
                    int(ff[1] * window_size[1] + np.sin(ff[2]) * 100)
                ),
                3
            )

    # draw particles
    for p in particles:

        pygame.draw.circle(
            window,
            (p[4], p[5], p[6]),
            (
                int(p[0] * window_size[1]),
                int(p[1] * window_size[1])
            ),
            #int(base_size + (p[2] ** 2 + p[3] ** 2) ** 0.5 * size_speed_mul)
            2
        )


    # update
    pygame.display.update()
    delta = clock.tick(fps) / 1000