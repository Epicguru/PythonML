
entities = []

target_frame_rate = 60
bg_colour = (255, 255, 255)
resolution = (600, 400)
running = True


def run():
    import pygame
    from game_entity import GameEntity

    print("Starting machine learning game...")
    pygame.init()

    # Create a clock to manage frame rate.
    clock = pygame.time.Clock()

    # Set up the screen
    screen = pygame.display.set_mode(resolution)

    # Start game loop.
    while running:

        # Wait for target time to achieve frame rate, and also get ms time to extract delta time.
        ms = clock.tick(target_frame_rate)
        dt = ms / 1000.0

        for event in pygame.event.get():
            for e in entities:
                if isinstance(e, GameEntity):
                    e.upon_event(event)

        for e in entities:
            if isinstance(e, GameEntity):
                e.update(dt)

        screen.fill(bg_colour)

        # Draw everything here...

        # Update the window display. Must always be called.
        pygame.display.flip()

    print("Game loop terminated, bye...")


if __name__ == "__main__":
    run()
