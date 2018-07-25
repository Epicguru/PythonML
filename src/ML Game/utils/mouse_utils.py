import pygame
import game_state as gs


def get_mouse_pos() -> (int, int):
    pass


def get_world_mouse_pos() -> (float, float):

    # First, get its pos in the game window...
    mx, my = pygame.mouse.get_pos()
    my = gs.resolution[1] - my

    # Subtract center
    cx, cy = gs.resolution[0] * 0.5, gs.resolution[1] * 0.5

    mx -= cx
    my -= cy

    mx += gs.camera_pos.get_x()
    my += gs.camera_pos.get_y()

    return (mx, my)
