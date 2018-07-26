from game_entity import GameEntity
import game_state as gs
import settings
import pygame
from utils.text_utils import *


class ActionDisplay(GameEntity):

    def __init__(self):

        self.fonts = ["Impact"]
        self.font_size = 24

        self.txt = [
            "Skip Turn",
            "Punch Target",
            "Heal Self"
        ]
        self.selected_txt = "--> "
        self.selected_colour = (0, 0, 0)
        self.normal_colour = (50, 50, 50)
        self.s_a = 0

    def late_render(self, screen: pygame.Surface):

        if gs.friendly_turn:

            sx = 20
            sy = 40

            for i, value in enumerate(self.txt):
                action = self.make_txt(i, value)
                draw_text(action, screen, (sx, sy))
                sy += action.get_height() + 2

    def upon_event(self, event: pygame.event):

        if event.type == pygame.KEYDOWN:
            if event.key == ord("w"):
                if self.s_a > 0:
                    self.s_a -= 1
            elif event.key == ord("s"):
                if self.s_a < len(self.txt) - 1:
                    self.s_a += 1

    def make_txt(self, index, text):

        return create_text(
            (self.selected_txt if self.s_a == index else "") + text,
            color=(self.selected_colour if self.s_a == index else self.normal_colour),
            fonts=self.fonts,
            size=self.font_size)
