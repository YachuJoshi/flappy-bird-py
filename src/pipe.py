from pygame import image, transform


class Pipe:
    def __init__(self, props):
        self.x = props.get("x")
        self.y = props.get("y")
        self.type = props.get("type")
        self.image = image.load("./images/pipe-red.png").convert_alpha()
        self.image = (
            self.image if self.type == "bottom" else transform.rotate(self.image, 180)
        )
        self.rect = self.image.get_rect(topleft=(self.x, self.y))
        self.speed = 2

    def draw(self, screen) -> None:
        screen.blit(self.image, self.rect)

    def update(self) -> None:
        self.rect.left -= self.speed

    def __repr__(self) -> str:
        return f"x: {self.x} y: {self.y} type: {self.type}"
