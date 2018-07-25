import pygame

# IMPORTANT:
# Full credit to https://nerdparadise.com/ for this code, I just shuffled it around a bit.

_cached_fonts = {}
_cached_text = {}


def make_font(fonts, size):
    available = pygame.font.get_fonts()
    choices = map(lambda x: x.lower().replace(' ', ''), fonts)
    for choice in choices:
        if choice in available:
            return pygame.font.SysFont(choice, size)
    return pygame.font.Font(None, size)


def get_font(font_preferences, size, cache: bool = True):
    global _cached_fonts
    key = str(font_preferences) + '|' + str(size)
    font = _cached_fonts.get(key, None)
    if font is None:
        font = make_font(font_preferences, size)
        if cache:
            _cached_fonts[key] = font
            print("Cached %s" % key)
    return font


def create_text(text, fonts=["Arial"], size=32, color=(0, 0, 0), cache: bool = True) -> pygame.Surface:
    global _cached_text
    key = '|'.join(map(str, (fonts, size, color, text)))
    image = _cached_text.get(key, None)
    if image is None:
        font = get_font(fonts, size)
        image = font.render(text, True, color)
        if cache:
            _cached_text[key] = image
    return image


def draw_text(text, screen: pygame.Surface, position):

    off_x = 0
    off_y = 0

    screen.blit(text,
                (position[0] + off_x, position[1] + off_y))
