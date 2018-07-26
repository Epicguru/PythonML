import window_control_entity
import camera_controller
import action_display
import game_state as gs
import game_manager
import input_helper
import battle_log

def add_entities():

    gs.camera_controller = camera_controller.CameraController()
    gs.action_display = action_display.ActionDisplay()

    gs.register_entity(gs.camera_controller)
    gs.register_entity(gs.action_display)
    gs.register_entity(window_control_entity.WindowControlEntity())


def run():
    import pygame
    from game_entity import GameEntity
    import time

    print("Starting machine learning game...")
    pygame.init()

    # Create a clock to manage frame rate.
    clock = pygame.time.Clock()

    # Set up the screen
    screen = pygame.display.set_mode(gs.resolution)

    # Add core entities.
    add_entities()

    # Start game manager
    game_manager.start_game()

    last_time = time.time()
    # Start game loop.
    while gs.running:

        # Wait for target time to achieve frame rate, and also get ms time to extract delta time.
        clock.tick(gs.target_frame_rate)
        time_now = time.time()
        dt = (time_now - last_time) * gs.time_scale
        last_time = time_now

        # Update title
        gs.frames_per_second = round(clock.get_fps())
        pygame.display.set_caption("ML Game: %sfps, cam @ %s" % (str(round(clock.get_fps())), gs.camera_pos))

        for event in pygame.event.get():
            for e in gs.entities:
                e.upon_event(event)

        game_manager.update(dt)
        for e in gs.entities:
            e.update(dt)

        screen.fill(gs.bg_colour)

        # Draw everything here...
        for e in gs.entities:
            e.render(screen)
        for e in gs.entities:
            e.late_render(screen)

        # Update the window display. Must always be called.
        pygame.display.flip()

    print("Game loop terminated, bye...")

    battle_log.save_datasets()

if __name__ == "__main__":

    run()
