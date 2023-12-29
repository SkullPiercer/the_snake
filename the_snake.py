from gameparts import Snake, Apple, clock, SPEED, handle_keys, screen, BOARD_BACKGROUND_COLOR
import pygame


def main():
    """Основной игровой цикл."""
    snake = Snake()
    apple = Apple()
    while True:
        clock.tick(SPEED)
        if apple.position in snake.positions:
            apple.randomize_position()
        snake.draw(screen)
        apple.draw(screen)
        handle_keys(snake)
        snake.move()
        if snake.game_over():
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        if snake.positions[0] == apple.position:
            apple.randomize_position()
            snake.eat()
        pygame.display.update()


if __name__ == '__main__':
    main()
