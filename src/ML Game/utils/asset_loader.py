import pygame
import os

images = {}


def load_image(path: str, use_cache=True, save_to_cache=True) -> pygame.Surface:
    """
    :param path: The path to the image, from within the assets/sprites folder. So to load 'assets/sprites/Foo.png'
    you would just pass 'Foo.png' as the path.
    :param use_cache: If true, the image will be loaded from cache if it is there. Otherwise it will always be loaded.
    :param save_to_cache: When true, if the image is loaded then it is saved to the cache to avoid future loading.
    :return: The Surface object, or None if the loading failed.
    """

    global images

    if use_cache and path in images:
        return images[path]

    full_path = os.path.join("assets", "sprites", path)
    try:
        loaded = pygame.image.load(full_path)

        if save_to_cache:
            # Add to cache
            images[path] = loaded
            print("Cached '%s'" % path)

        return loaded
    except pygame.error:
        print("ERROR: Failed to load image from path '%s'" % path)
        return None
