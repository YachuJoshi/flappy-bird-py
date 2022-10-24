# pylint: disable=E1101

import sys
from typing import List, Type
from random import randint
import pygame
from src.bird import Bird
from src.pipe import Pipe
from src.screen import init
from src.base import GAP, SCREEN_HEIGHT, SCREEN_WIDTH
from src.audio import hit_audio, jump_audio, point_audio
from src.texts import font, play_again_text, play_again_text_rect

caption: str = "Flappy Bird"
icon = pygame.image.load("./favicon.ico")
screen, clock = init(caption, icon)

foreground = pygame.image.load("./images/base.png").convert_alpha()
foreground_rect = foreground.get_rect(bottomleft=(0, 512))

background = pygame.image.load("./images/background-night.png").convert_alpha()

game_over = pygame.image.load("./images/gameover.png").convert_alpha()
game_over_rect = game_over.get_rect(
    center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 120)
)

score: int = 0
bird: Type[Bird] = None
game_active: bool = True
top_pipes: List[Type[Pipe]] = []
bottom_pipes: List[Type[Pipe]] = []


# Custom Event For Producing Pipes
pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(pipe_timer, 2000)


def init_game() -> None:
    global score, game_active, bird, top_pipes, bottom_pipes
    score = 0
    bird = Bird()
    top_pipes = []
    bottom_pipes = []
    game_active = True


def generate_pipes() -> None:
    pipe_x = SCREEN_WIDTH + 10
    pipe_top_y = randint(-200, -50)
    pipe_bottom_y = pipe_top_y + GAP

    top_pipes.append(Pipe({"x": pipe_x, "y": pipe_top_y, "type": "top"}))
    bottom_pipes.append(Pipe({"x": pipe_x, "y": pipe_bottom_y, "type": "bottom"}))


def draw() -> None:
    if not bird:
        return

    for top_pipe, bottom_pipe in zip(top_pipes, bottom_pipes):
        top_pipe.draw(screen)
        bottom_pipe.draw(screen)

    bird.draw(screen)


def update() -> None:
    global game_active, score
    if not bird:
        return

    bird.update()

    for top_pipe, bottom_pipe in zip(top_pipes, bottom_pipes):
        top_pipe.update()
        bottom_pipe.update()

        if (
            top_pipe.rect.left == 80
            and bird.rect.top > top_pipe.rect.bottom
            and bird.rect.bottom < bottom_pipe.rect.top
        ):
            score += 1
            point_audio.play()

        # Remove pipes if beyond the screen
        if top_pipe.rect.right < -10:
            top_pipes.pop(0)
            bottom_pipes.pop(0)

        # Check Collision
        if bird.check_collision(top_pipe) or bird.check_collision(bottom_pipe):
            hit_audio.play()
            game_active = False


def main() -> None:
    global game_active, score
    init_game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pipe_timer and game_active:
                generate_pipes()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if game_active:
                    bird.flap()
                    jump_audio.play()
                else:
                    init_game()

        if game_active:
            screen.blit(background, (0, 0))

            draw()
            update()

            score_text = font.render(f"{score}", False, "white")
            score_text_rect = score_text.get_rect(center=(SCREEN_WIDTH / 2, 70))
            screen.blit(score_text, score_text_rect)

            # Foreground
            screen.blit(foreground, foreground_rect)
            foreground_rect.left -= 2

            if foreground_rect.right - 10 < SCREEN_WIDTH:
                foreground_rect.left = 0

            if bird.check_collision(foreground_rect):
                hit_audio.play()
                game_active = False
        else:
            screen.blit(background, (0, 0))
            screen.blit(foreground, foreground_rect)
            screen.blit(game_over, game_over_rect)
            score_text = font.render(f"{score}", False, "white")
            score_text_rect = score_text.get_rect(
                center=(SCREEN_WIDTH / 2, (SCREEN_HEIGHT / 2) - 50)
            )
            screen.blit(score_text, score_text_rect)
            screen.blit(play_again_text, play_again_text_rect)

        pygame.display.update()
        clock.tick(60)


if __name__ == "__main__":
    main()
