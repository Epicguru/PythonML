from game_entity import GameEntity
import utils.math_utils
import utils.asset_loader
from utils.math_utils import *
from utils import asset_loader
from utils.mouse_utils import *
from utils.text_utils import *
from sprite import Sprite
import game_state as gs
import settings
import random
import sprite


class Agent(GameEntity):

    def __init__(self, index: int):

        self.index = index
        self.highlighted = False
        self.is_friendly = True
        self.name = "Random Guy"
        self.max_health = 100.0
        self.health = 100.0
        self.weapon = None
        self.body_sprite = None
        self.label_sprite = Sprite(None)
        self.highlight_sprite = Sprite(asset_loader.load_image("Agent Highlight.png"))
        self.position = Vector2(0, 0)
        self.offset = Vector2(0, 0)
        self.rumble = Vector2(0, 0)
        self.rumble_mag = 0.0
        self.rumble_decay = 12.0
        self.attack_offset = 0.0
        self.has_died = False
        self.base_attack_damage = 50.0

        # Register
        gs.register_entity(self)

    def is_dead(self):
        return self.health <= 0

    def damage(self, hp: float):
        self.health = max(self.health - hp, 0.0)

    def attack_anim(self, direction):
        self.attack_offset = direction

    def update(self, dt: float):

        if self.body_sprite is not None:
            self.body_sprite.set_pivot(0.5, 0.5)
            self.body_sprite.set_position(self.position)

        self.rumble_mag = lerp(self.rumble_mag, 0.0, dt * self.rumble_decay)
        self.rumble.set_x(random.randrange(-100, 101))
        self.rumble.set_y(random.randrange(-100, 101))
        self.rumble.normalize()
        self.rumble *= self.rumble_mag
        self.attack_offset = lerp(self.attack_offset, 0.0, dt * 30.0)
        self.offset.set(self.rumble)
        self.offset.inc_x(self.attack_offset)

        h_active = (self.highlighted
                    or (self.is_friendly and
                        gs.friendly_turn and
                        len(gs.friendlies) > 0 and
                        gs.friendlies[gs.turn_index] == self)
                    or (not self.is_friendly and
                        not gs.friendly_turn and
                        len(gs.enemies[gs.current_stage]) > 0 and
                        gs.enemies[gs.current_stage][gs.turn_index] == self))

        if h_active:
            self.highlight_sprite.position.set(self.position + self.offset)
            self.highlight_sprite.to_bottom()
            self.highlight_sprite.set_pivot(0.5, 0.5)
        self.highlight_sprite.enabled = h_active

        self.label_sprite.set_image(create_text("%s HP" % str(math.ceil(self.health)), size=19, color=(10, 20, 0), fonts=["Impact"]))
        self.label_sprite.set_pivot(0.5, 0.5)
        self.label_sprite.use_late_render = True
        self.label_sprite.set_position(self.position + Vector2(100 * self.label_direction(), 60))

        if self.is_dead():

            if not self.has_died:
                self.died()
                self.has_died = True
                if gs.selected_agent == self:
                    gs.selected_agent = None

            if self.rumble_mag <= 0.01:
                super().remove()
                self.body_sprite.remove()
                self.highlight_sprite.remove()
                self.label_sprite.remove()

            return

        mx, my = get_world_mouse_pos()
        if self.body_sprite.get_bounds().collidepoint(mx, my):
            self.highlighted = True
            gs.selected_agent = self
        else:
            self.highlighted = False
            if gs.selected_agent == self:
                gs.selected_agent = None

    def render(self, screen: pygame.Surface):

        pos = (self.position + Vector2(185 * self.health_bar_direction(), 50))
        size = (148, 16)
        inner_size = (140 * (self.health / self.max_health), 8)
        x, y = sprite.translate((pos.get_x(), pos.get_y()), size, (0, 1))
        pygame.draw.rect(screen, (20, 20, 20), pygame.Rect((x, y), size))
        pygame.draw.rect(screen, (20, 255, 20), pygame.Rect((x + 4, y + 4), inner_size))

    def health_bar_direction(self) -> float:
        return -1

    def label_direction(self):
        return -1

    def died(self):
        pass

    def to_top(self):
        super().to_top()

        if self.body_sprite is not None:
            self.body_sprite.to_top()

    def to_bottom(self):
        super().to_bottom()

        if self.body_sprite is not None:
            self.body_sprite.to_bottom()
            self.highlight_sprite.to_bottom()

    def get_damage(self, action_index):
        return self.base_attack_damage

    def __str__(self):
        return "Friendly agent '%s'" % self.name if self.is_friendly else "Enemy agent '%s'" % self.name


class FAgent(Agent):

    def create(self):

        self.is_friendly = True
        self.body_sprite = Sprite(utils.asset_loader.load_image("Friendly.png"))
        self.name = "Good Guy #" + str(self.index + 1)

        self.health = settings.agent_base_friendly_health
        self.max_health = settings.agent_base_friendly_health
        self.base_attack_damage = settings.agent_base_friendly_damage

    def damage(self, hp: float):
        super().damage(hp)
        self.rumble_mag = 20.0

    def died(self):
        super().died()

        gs.friendlies.remove(self)

    def update(self, dt: float):

        target = Vector2(
            gs.current_stage * settings.stage_sep_distance + self.index * settings.agent_horizontal_difference,
            self.index * settings.agent_height_difference)
        calculated_pos = lerp(self.position, target, dt * 10.0)
        self.position.set(calculated_pos + self.offset)

        super().update(dt)


class EAgent(Agent):

    def __init__(self, index: int, stage: int, health: float):
        super().__init__(index)

        self.stage = stage

        self.health = health
        self.max_health = health
        self.base_attack_damage = settings.agent_base_enemy_damage

    def create(self):
        self.is_friendly = False
        self.body_sprite = Sprite(utils.asset_loader.load_image("Enemy.png"))
        self.name = "Bad Guy #" + str(self.index + 1)

    def damage(self, hp: float):
        super().damage(hp)
        self.rumble_mag = 20.0

    def died(self):
        super().died()
        gs.enemies[self.stage].remove(self)

    def update(self, dt: float):

        target = Vector2(
            self.stage * settings.stage_sep_distance - self.index * settings.agent_horizontal_difference + settings.agent_side_separation,
            self.index * settings.agent_height_difference)
        calculated_pos = lerp(self.position, target, dt * 10.0)
        self.position.set(calculated_pos + self.offset)

        super().update(dt)

    def health_bar_direction(self):
        return 0.2

    def label_direction(self):
        return 1.1
