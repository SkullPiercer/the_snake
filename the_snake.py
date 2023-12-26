from random import choice, randint
import pygame

# Инициализация PyGame
pygame.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона - черный
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Скорость движения змейки
SPEED = 20

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()


class GameObject:
    """Родительский класс для описания объектов на игровом поле."""

    def __init__(self):
        """Инициализация объекта."""
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )
        self.body_color = None

    def draw(self, surface):
        """Абстрактный метод отрисовки объектов."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко на игровом поле."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__()
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Генерация случайной позиции для яблока."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Отрисовка яблока на экране."""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку на игровом поле."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__()
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = choice((UP, DOWN, RIGHT, LEFT))
        self.body_color = (0, 255, 0)
        self.last = 0

    def update_direction(self):
        """Обновление направления движения змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def game_over(self):
        """Проверка на окончание игры (столкновение с самой собой)."""
        head = self.get_head_position()
        if head in self.positions[1:]:
            return True

    def move(self):
        """Джение змейки."""
        self.update_direction()
        x, y = self.get_head_position()
        if self.direction == RIGHT:
            x += GRID_SIZE
            if x >= SCREEN_WIDTH:
                x = 0
        elif self.direction == UP:
            y -= GRID_SIZE
            if y < 0:
                y = SCREEN_HEIGHT - GRID_SIZE
        elif self.direction == DOWN:
            y += GRID_SIZE
            if y >= SCREEN_HEIGHT:
                y = 0
        elif self.direction == LEFT:
            x -= GRID_SIZE
            if x < 0:
                x = SCREEN_WIDTH - GRID_SIZE
        self.positions.insert(0, (x, y))
        self.last = self.positions[-1]
        self.positions.pop()

    def eat(self):
        """Обработка поедания яблока и увеличения размера"""
        x, y = self.positions[-1]
        self.length += 1
        if self.direction == RIGHT:
            self.positions.append((x - 20, y))
        elif self.direction == UP:
            self.positions.append((x, y + 20))
        elif self.direction == DOWN:
            self.positions.append((x, y - 20))
        elif self.direction == LEFT:
            self.positions.append((x + 20, y))

    def draw(self, surface):
        """Отрисовка змейки на экране."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Получение позиции головы змейки."""
        return self.positions[0]

    def reset(self):
        """Перезапуск игрового цикла."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice((UP, DOWN, RIGHT, LEFT))
        self.next_direction = RIGHT


def handle_keys(game_object):
    """Функция обработки действий пользователя."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
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
