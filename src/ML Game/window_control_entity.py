import pygame
import random
from utils.asset_loader import load_image
from utils.text_utils import *

from agents import *


class WindowControlEntity(GameEntity):

    def create(self):

        for i in range(100):
            x = random.randrange(0, 19) * 64
            y = random.randrange(0, 19) * 64

            spr = Sprite(load_image("Test.png"), position=Vector2(x, y))
            spr.set_pivot(0.5, 0.5)

    def upon_event(self, event: pygame.event):

        if event.type == pygame.QUIT:
            gs.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if gs.time_scale == settings.boosted_time_scale:
                    gs.time_scale = 1.0
                else:
                    gs.time_scale = settings.boosted_time_scale

    def late_render(self, screen: pygame.Surface):

        text = create_text("Stage %d/%d" % (gs.current_stage + 1, settings.total_stages), size=24)
        draw_text(text, screen, (0, 0))

        pass
