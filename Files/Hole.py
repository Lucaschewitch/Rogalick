import pygame


class Hole(pygame.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        super().__init__()
        self.game = game
        self.rect = pygame.Rect(x, y, w, h)
        # Сохраняем параметры для возможного внешнего использования
        self.x = x
        self.y = y
        self.w = w
        self.h = h

        # Автоматически добавляем себя в группу отверстий игры
        game.holes.add(self)

    def update(self):
        # Уничтожаем врагов, попавших в яму (оптимизированная проверка)
        pygame.sprite.spritecollide(self, self.game.enemies, True)

        # Обработка столкновения игрока с ямой
        player_collision = (
                not self.game.player.flying
                and pygame.sprite.spritecollide(self, self.game.players, False)
        )

        if player_collision:
            # Сбрасываем позицию игрока и уменьшаем жизни
            self.game.player.resetLocation()
            self.game.player.life -= 2

            # Сбрасываем позиции всех выживших врагов
            for enemy in self.game.enemies:
                enemy.resetLocation()