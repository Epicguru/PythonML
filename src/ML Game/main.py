import window_control_entity
import game_state as gs


def add_entities():

    gs.entities.append(window_control_entity.WindowControlEntity())

    for e in gs.entities:
        e.init()


def run():
    import pygame
    from game_entity import GameEntity
    import time

    print("Starting machine learning game...")
    pygame.init()

    # Local variables
    last_time = time.time()
    frame_rate_timer = 0.0
    frame_rate_counter = 0

    # Create a clock to manage frame rate.
    clock = pygame.time.Clock()

    # Set up the screen
    screen = pygame.display.set_mode(gs.resolution)

    # Add core entities.
    add_entities()

    # Start game loop.
    while gs.running:

        # Wait for target time to achieve frame rate, and also get ms time to extract delta time.
        ms = clock.tick(gs.target_frame_rate)
        time_now = time.time()
        dt = time_now - last_time
        last_time = time_now

        # Update frame rate stats
        frame_rate_timer += dt
        frame_rate_counter += 1
        if frame_rate_timer >= 1.0:
            frame_rate_timer -= 1.0
            gs.frames_per_second = frame_rate_counter
            frame_rate_counter = 0
            pygame.display.set_caption("ML Game: %sfps" % str(gs.frames_per_second))

        for event in pygame.event.get():
            for e in gs.entities:
                if isinstance(e, GameEntity):
                    e.upon_event(event)

        for e in gs.entities:
            if isinstance(e, GameEntity):
                e.update(dt)

        screen.fill(gs.bg_colour)

        # Draw everything here...
        for e in gs.entities:
            if isinstance(e, GameEntity):
                e.render(screen)
        # Update the window display. Must always be called.
        pygame.display.flip()

    print("Game loop terminated, bye...")


def quit_game():
    global running
    running = False


if __name__ == "__main__":

    run()
