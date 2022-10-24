from pygame.font import Font
from src.base import SCREEN_HEIGHT, SCREEN_WIDTH

font = Font("./font/FlappyBird.ttf", 50)
play_again_font = Font("./font/FlappyBird.ttf", 30)

play_again_text = play_again_font.render("Click To Play Again", False, "orange")
play_again_text_rect = play_again_text.get_rect(
    center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
)
