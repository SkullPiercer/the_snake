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

# Цвета объектов
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (93, 216, 228)

# Словарь для обработки нажатых игроком клавиш
KEY_MAPPING = {
    (LEFT, pygame.K_UP): UP,
    (LEFT, pygame.K_DOWN): DOWN,
    (LEFT, pygame.K_LEFT): LEFT,
    (UP, pygame.K_UP): UP,
    (UP, pygame.K_LEFT): LEFT,
    (UP, pygame.K_RIGHT): RIGHT,
    (DOWN, pygame.K_DOWN): DOWN,
    (DOWN, pygame.K_LEFT): LEFT,
    (DOWN, pygame.K_RIGHT): RIGHT,
    (RIGHT, pygame.K_UP): UP,
    (RIGHT, pygame.K_DOWN): DOWN,
    (RIGHT, pygame.K_RIGHT): RIGHT,
}

class GameObject:
    """Родительский класс для описания объектов на игровом поле."""

    def __init__(self, body_color=None):
        """Инициализация объекта."""
        self.body_color = body_color
        self.position = (
            SCREEN_WIDTH // 2,
            SCREEN_HEIGHT // 2
        )

    def draw(self, surface):
        """Абстрактный метод отрисовки объектов."""
        pass


class Apple(GameObject):
    """Класс, представляющий яблоко на игровом поле."""

    def __init__(self):
        """Инициализация яблока."""
        super().__init__()
        self.body_color = RED
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
        pygame.draw.rect(surface, BLUE, rect, 1)


class Snake(GameObject):
    """Класс, представляющий змейку на игровом поле."""

    def __init__(self):
        """Инициализация змейки."""
        super().__init__()
        self.body_color = GREEN
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = choice((UP, DOWN, RIGHT, LEFT))
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
        first_pos, second_pos = self.get_head_position()
        next_step = {
            RIGHT: lambda x, y: (x + GRID_SIZE, y) if x <= SCREEN_WIDTH else (0, y),
            UP: lambda x, y: (x, y - GRID_SIZE) if y >= 0 else (x, SCREEN_HEIGHT - GRID_SIZE),
            DOWN: lambda x, y: (x, y + GRID_SIZE) if y <= SCREEN_HEIGHT else (x, 0),
            LEFT: lambda x, y: (x - GRID_SIZE, y) if x > 0 else (SCREEN_WIDTH - GRID_SIZE, y)
        }
        result = next_step[self.direction]
        self.positions.insert(0, (result(first_pos, second_pos)))
        self.last = self.positions[-1]
        self.positions.pop()

    def eat(self):
        """Обработка поедания яблока и увеличения размера"""
        x, y = self.positions[-1]
        self.length += 1
        directions = {
            RIGHT: (x - 20, y),
            UP: (x, y + 20),
            DOWN: (x, y - 20),
            LEFT: (x + 20, y)
        }
        position = directions[self.direction]
        self.positions.append(position)

    def draw(self, surface):
        """Отрисовка змейки на экране."""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BLUE, rect, 1)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, BLUE, head_rect, 1)

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
            current_direction = game_object.direction
            new_direction = KEY_MAPPING.get((current_direction, event.key), current_direction)
            game_object.next_direction = new_direction


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
