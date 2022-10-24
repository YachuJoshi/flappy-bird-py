from pygame import image, transform
from src.base import SCREEN_HEIGHT

GRAVITY = 0.4


class Bird:
    def __init__(self) -> None:
        self.x = 100
        self.y = SCREEN_HEIGHT / 2 - 100
        self.speed = 0
        self.downflap_image = image.load(
            "./images/redbird-downflap.png"
        ).convert_alpha()
        self.midflap_image = image.load("./images/redbird-midflap.png").convert_alpha()
        self.upflap_image = image.load("./images/redbird-upflap.png").convert_alpha()
        self.images = [self.midflap_image, self.downflap_image, self.upflap_image]
        self.rect = self.midflap_image.get_rect(center=(self.x, self.y))
        self.is_falling = True
        self.index = 0

    def draw(self, screen):
        angle = -60 if self.is_falling else 30
        image = transform.rotate(self.images[int(self.index)], angle)

        screen.blit(image, self.rect)

    def update(self):
        # Update Bird Position
        self.speed += GRAVITY
        self.rect.bottom += self.speed

        # Update Sprite
        self.index += 0.1
        if self.index >= len(self.images):
            self.index = 0

        if self.speed > 6:
            self.is_falling = True
        else:
            self.is_falling = False

    def flap(self):
        self.speed = -5

    def check_collision(self, game_asset_rect):
        return self.rect.colliderect(game_asset_rect)
