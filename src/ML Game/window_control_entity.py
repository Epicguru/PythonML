import pygame
import random
from utils.asset_loader import load_image
from utils.text_utils import *
from utils.mouse_utils import *

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

        mx, my = get_world_mouse_pos()
        enemies = gs.enemies[gs.current_stage]
        if len(enemies) > 0:
            for e in enemies:
                if e.body_sprite.get_bounds().collidepoint(mx, my):
                    e.highlighted = True
                    selected_text = create_text(("" if e.is_friendly else "Enemy '" + e.name + "' : %d/%d HP" % (e.health, e.max_health)), size=24, fonts=["Calibri"])
                    draw_text(selected_text, screen, (5, 30))
                else:
                    e.highlighted = False

        stage_text = create_text("Stage %d/%d" % (gs.current_stage + 1, settings.total_stages), size=24)
        draw_text(stage_text, screen, (5, 0))

        pass
