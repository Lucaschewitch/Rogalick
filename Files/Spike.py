import pygame


class Spike(pygame.sprite.Sprite):
    # Общие ресурсы для всех экземпляров
    SPIKE_STATES = []

    @classmethod
    def load_resources(cls):
        if not cls.SPIKE_STATES:  # Загружаем только один раз
            image = pygame.image.load('../Assets/Spikes.png')
            for i in range(3):
                rect = pygame.Rect(i * 17, 0, 16, 16)
                cls.SPIKE_STATES.append(image.subsurface(rect))

    def __init__(self, game, x, y, width, height, spike_type):
        super().__init__()
        self.load_resources()  # Инициализация ресурсов

        self.game = game
        self.rect = pygame.Rect(x, y, width, height)
        self.spike_type = spike_type
        self.width = width
        self.height = height

        # Для совместимости с существующим кодом отрисовки
        self.spikeStates = self.SPIKE_STATES

        self.active = (spike_type == 'on')
        self.inversion_timer = 120
        self.damage_cooldown = 0

        game.spikes.add(self)

    def getRenderImg(self):
        """Совместимость с существующим кодом отрисовки"""
        if self.active:
            return 2
        return 1 if self.inversion_timer <= 60 else 0

    def toggle_state(self):
        # Исправлено имя метода на оригинальное: playSfx вместо play_sfx
        self.game.menu.sound.playSfx(3)
        self.active = not self.active

    def apply_damage(self, target):
        if self.damage_cooldown <= 0:
            target.life -= 1
            self.damage_cooldown = 20  # Задержка между уроном
            return True
        return False

    def update(self):
        # Обновление таймеров
        self.inversion_timer = max(0, self.inversion_timer - 1)
        self.damage_cooldown = max(0, self.damage_cooldown - 1)

        # Автоматическая инверсия состояния
        if self.inversion_timer == 0:
            self.inversion_timer = 120
            self.toggle_state()

        # Обработка столкновений с игроком
        player_collision = (
                self.active and
                pygame.sprite.spritecollide(self, self.game.players, False) and
                not self.game.player.flying
        )
        if player_collision:
            self.apply_damage(self.game.player)

        # Обработка столкновений с врагами
        for enemy in self.game.enemies:
            if self.active and self.rect.colliderect(enemy.rect):
                self.apply_damage(enemy)