import pygame
from textEngine import *


class Hud:
    # Константы для позиционирования элементов
    HEART_OFFSET = 30
    BOOK_POSITION = (10, 440)
    COOLDOWN_BAR_POS = (10, 475)
    EFFECT_BAR_POS = (10, 435)
    BAR_WIDTH = 30
    DEATH_TEXT_POS = (225, 175)
    DEATH_SURFACE_HEIGHT_OFFSET = 340

    def __init__(self, game):
        self.game = game
        self.you_died = False
        self.death_alpha = 0
        self.death_counter = 0

        # Загрузка и подготовка изображений
        self.heart_images = self._load_heart_images()
        self.boss_heart_images = self._load_boss_heart_images()  # Не используется, но сохранен
        self.death_text = self._prepare_death_text()

        # Инициализация элементов интерфейса
        self.cooldown_bar = pygame.Rect(self.COOLDOWN_BAR_POS, (3, 3))
        self.effect_bar = pygame.Rect(self.EFFECT_BAR_POS, (3, 3))

        # Инициализация счетчиков
        self.full_hearts = 0
        self.half_hearts = 0
        self.empty_hearts = 0

    def _load_heart_images(self):
        """Загрузка и масштабирование изображений сердец"""
        heart_img = pygame.image.load('../Assets/heart.png').convert_alpha()
        stages = []
        for x_pos in [0, 16, 32]:
            frame = heart_img.subsurface(pygame.Rect(x_pos, 0, 13, 12))
            stages.append(pygame.transform.scale(frame, (26, 24)))
        return stages

    def _load_boss_heart_images(self):
        """Загрузка изображений сердец босса (сохранено для совместимости)"""
        heart_img = pygame.image.load('../Assets/heartBoss.png').convert_alpha()
        return [
            pygame.transform.scale(heart_img.subsurface(pygame.Rect(x, 0, 13, 12)), (26, 24))
            for x in [0, 16, 32]
        ]

    def _prepare_death_text(self):
        """Подготовка текста 'POTRACHENO'"""
        text_surface = textGui().text(
            'POTRACHENO',
            color=(140, 0, 0),
            antialias=False,
            background=(255, 255, 255)
        )
        text_surface.set_colorkey((255, 255, 255))
        return pygame.transform.scale(text_surface, (295, 120))

    def update(self):
        """Обновление состояния HUD"""
        self._update_hearts()
        self._update_bars()

        # Обработка состояния смерти игрока
        if self.game.player.life <= 0:
            self._handle_death_state()

    def _update_hearts(self):
        """Расчет количества сердец разного типа"""
        life = self.game.player.life
        max_life = self.game.player.maxLife

        self.full_hearts = min(life // 2, max_life // 2)
        self.half_hearts = 1 if life % 2 == 1 else 0
        self.empty_hearts = (max_life // 2) - self.full_hearts - self.half_hearts

    def _update_bars(self):
        """Обновление состояния полосок способностей"""
        player = self.game.player
        self.cooldown_bar.width = self._calculate_bar_width(
            player.bookMagicCooldown,
            player.bookMagicCooldownDefault
        )
        self.effect_bar.width = self._calculate_bar_width(
            player.effectTime,
            player.effectTimeDefault
        )

    def _calculate_bar_width(self, current, maximum):
        """Расчет ширины полосы состояния"""
        return max(1, int(30 * current / maximum)) if maximum > 0 else 0

    def _handle_death_state(self):
        """Обработка логики смерти игрока"""
        if not self.you_died:
            self.game.menu.sound.playSfx(2)
            self.you_died = True

        if self.death_alpha < 200:
            self.death_alpha += 2
        else:
            self.death_counter += 1

        if self.death_counter >= 70:
            self.game.done = True
            self.game.gameRun(self.game.saveName)

    def draw(self):
        """Отрисовка всех элементов HUD"""
        self._draw_hearts()
        self._draw_book()
        self._draw_bars()

        if self.game.player.life <= 0:
            self._draw_death_screen()

    def _draw_hearts(self):
        """Отрисовка сердец здоровья"""
        x_position = 0
        heart_types = [
            (self.full_hearts, 0),  # Полные сердца
            (self.half_hearts, 1),  # Полусердца
            (self.empty_hearts, 2)  # Пустые сердца
        ]

        for count, heart_index in heart_types:
            for _ in range(count):
                self.game.screen.blit(self.heart_images[heart_index], (x_position, 0))
                x_position += self.HEART_OFFSET

    def _draw_book(self):
        """Отрисовка книги способностей"""
        book_index = 1 if self.game.player.effectTime != 0 else 0
        book_img = pygame.transform.scale(
            self.game.player.bookImg[book_index],
            (32, 32)
        )
        self.game.screen.blit(book_img, self.BOOK_POSITION)

    def _draw_bars(self):
        """Отрисовка полосок перезарядки"""
        if self.effect_bar.width > 1:
            pygame.draw.rect(self.game.screen, (255, 0, 0), self.effect_bar)
        if self.cooldown_bar.width > 1:
            pygame.draw.rect(self.game.screen, (0, 255, 0), self.cooldown_bar)

    def _draw_death_screen(self):
        """Отрисовка экрана смерти"""
        death_surface = pygame.Surface(
            (self.game.screenSize[0], self.game.screenSize[1] - self.DEATH_SURFACE_HEIGHT_OFFSET)
        )
        death_surface.fill((0, 0, 0))
        death_surface.set_alpha(self.death_alpha)

        self.death_text.set_alpha(self.death_alpha)
        self.game.screen.blit(death_surface, (0, 175))
        self.game.screen.blit(self.death_text, self.DEATH_TEXT_POS)