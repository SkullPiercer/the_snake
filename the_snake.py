from gameparts import Apple, Snake, screen, SPEED, handle_keys, clock, BOARD_BACKGROUND_COLOR
import pygame


def main():
    # Тут нужно создать экземпляры классов
    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED - 10)
        apple.draw(screen)
        snake.draw(screen)
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

