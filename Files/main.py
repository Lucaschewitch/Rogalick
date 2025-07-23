import pygame
from textEngine import textGui
from glob import glob
from Interpreter import Interpreter
from os import name
from saveGetter import saveGetter
from MenuUI import *
from Game import game
from Sounds import Sound


class MainMenu:
    MENU_PAGES = ['new', 'load', 'options', 'credits', 'quit']
    DIFFICULTIES = ['easy', 'normal', 'hard']
    LOGO_ANIMATION_RANGE = (0, 20)

    def __init__(self):
        # Инициализация основных компонентов
        self.data = Interpreter()
        self.screen = pygame.display.set_mode((720, 480))
        self.sound = Sound()
        self.textGui = textGui()
        self.game = game(self)

        # Загрузка настроек
        self.difficultySelected = self.data.getParameter('difficulty')
        self.musicValue = self.data.getParameter('music')
        self.sfxValue = self.data.getParameter('sfx')

        # Инициализация элементов интерфейса
        self.buttons = []
        self.menuButtons = []
        self.bigButtons = []
        self.sliders = []
        self.texts = {}
        self.images = []

        # Состояние меню
        self.logoPos = [0, 0]
        self.animBool = True
        self.backgroundMenu = False

        # Словарь страниц меню
        self.menuPage = {
            'new': False,
            'load': False,
            'options': False,
            'credits': False,
            'quit': False
        }

        # Загрузка ресурсов
        self.loadImages()
        self.mainMenu()

        # Запуск музыки
        self.sound.playMusic(0, 2)

    def loadImages(self):
        """Загрузка графических ресурсов для меню"""
        # Загрузка логотипа
        self.logo = pygame.image.load('../Assets/menuAssets/logo.png')

        # Загрузка остальных изображений
        self.images = []
        if name == 'nt':  # Windows
            for file in glob('../Assets/menuAssets/*.png'):
                self.images.append(pygame.image.load(file))
            if len(self.images) > 15:
                self.images[14], self.images[15] = self.images[15], self.images[14]
        else:  # Другие ОС
            tempList = []
            for file in glob('../Assets/menuAssets/*.png'):
                tempList.append(file)
            tempList.sort()
            for file in tempList:
                self.images.append(pygame.image.load(file))

    def mainMenu(self):
        """Создание кнопок главного меню"""
        y_pos = 180
        menuButton(self, 10, y_pos, 'New Game', 'new', 'menuButtons')
        menuButton(self, 10, y_pos + 60, 'Load Game', 'load', 'menuButtons')
        menuButton(self, 10, y_pos + 120, 'Options', 'options', 'menuButtons')
        menuButton(self, 10, y_pos + 180, 'Credits', 'credits', 'menuButtons')
        menuButton(self, 10, y_pos + 240, 'Quit', 'quit', 'menuButtons')

    def clear(self):
        """Очистка элементов интерфейса"""
        self.bigButtons.clear()
        self.sliders.clear()
        self.buttons.clear()
        self.texts.clear()

    def update(self):
        """Обновление состояния меню"""
        # Обновление элементов интерфейса
        for element in self.menuButtons + self.bigButtons + self.buttons + self.sliders:
            element.update()

        # Обновление анимации логотипа
        if self.animBool:
            self.logoPos[1] += 0.5
        else:
            self.logoPos[1] -= 0.5

        if self.logoPos[1] == 20 or self.logoPos[1] == 0:
            self.animBool = not self.animBool

        # Обновление настроек громкости
        if hasattr(self, 'sMusic') and hasattr(self, 'sSfx'):
            self.musicValue = self.sMusic.getValue()
            self.sfxValue = self.sSfx.getValue()
            self.data.updateParameter('music', self.musicValue)
            self.data.updateParameter('sfx', self.sfxValue)

        # Проверка музыки
        if self.sound.musicChannel.get_sound() != self.sound.musics[2]:
            self.sound.playMusic(0, 2)

        self.sound.update()

    def draw(self):
        """Отрисовка меню"""
        self.screen.fill((28, 17, 23))

        # Фоновое изображение
        if self.backgroundMenu:
            self.screen.blit(self.images[8], (350, 50))

        # Отрисовка элементов интерфейса
        for element in self.menuButtons + self.buttons + self.bigButtons + self.sliders:
            element.draw()

        # Отрисовка текста
        for key, value in self.texts.items():
            if key == 'difficulty':
                text_content = self.difficulty('return')
            else:
                text_content = value[0]
            self.screen.blit(self.textGui.text(text_content, color=(28, 17, 23)), value[1])

        # Отрисовка логотипа
        self.screen.blit(self.logo, self.logoPos)

    def newPage(self):
        """Отображение страницы новой игры"""
        if not self.menuPage['new']:
            self.clear()
            self.backgroundMenu = True
            bigButton(self, 370, 70, ['../Assets/character1.png'], '1 Player')
            bigButton(self, 520, 70, ['../Assets/character1.png', '../Assets/character2.png'], '2 Players')
            self.texts['Text'] = ['         Unavaible', (385, 230)]
            Button(self, 410, 340, 'self.menu.game.gameRun()', [self.images[15], self.images[15]])
            self.menuPage['new'] = True

    def loadPage(self):
        """Отображение страницы загрузки"""
        if not self.menuPage['load']:
            self.clear()
            self.backgroundMenu = True
            Button(self, 365, 70, image=[self.images[10], self.images[11]], text='Slot 1', selectable=True)
            Button(self, 365, 155, image=[self.images[10], self.images[11]], text='Slot 2', selectable=True)
            Button(self, 365, 240, image=[self.images[10], self.images[11]], text='Slot 3', selectable=True)
            Button(self, 405, 355, image=[self.images[5], self.images[5]], action='self.menu.load()')
            self.menuPage['load'] = True

    def optionsPage(self):
        """Отображение страницы настроек"""
        if not self.menuPage['options']:
            self.clear()
            self.backgroundMenu = True
            Button(self, 365, 70, image=[self.images[11], self.images[11]], text='Music')
            self.sMusic = Slider(self, 370, 155, 0, 100)
            Button(self, 365, 200, image=[self.images[11], self.images[11]], text='Sound Effects')
            self.sSfx = Slider(self, 370, 285, 0, 100)
            Button(self, 365, 320, image=[self.images[11], self.images[11]], text='Difficulty')
            Button(self, 375, 400, image=[self.images[4], self.images[4]])
            Button(self, 385, 401, image=[self.images[0], self.images[0]], action='self.menu.difficulty("down")')
            Button(self, 625, 401, image=[self.images[1], self.images[1]], action='self.menu.difficulty("up")')
            self.texts['difficulty'] = ('', (461, 391))
            self.menuPage['options'] = True

    def creditsPage(self):
        """Отображение страницы с благодарностями"""
        if not self.menuPage['credits']:
            self.clear()
            self.backgroundMenu = True
            Button(self, 365, 70, image=[self.images[11], self.images[11]], text='Made By:')
            self.texts['credit1'] = ('Lucaschewitch', (390, 150))
            self.texts['credit2'] = ('(Menu, code,', (390, 180))
            self.texts['credit3'] = ('level design)', (390, 210))
            self.texts['credit4'] = ('J_Giaco', (390, 250))
            self.texts['credit5'] = ('(Boss design)', (390, 280))
            self.texts['credit6'] = ('0x72', (390, 320))
            self.texts['credit7'] = ('(Tilesets)', (390, 350))
            self.texts['credit8'] = ('Kryse', (560, 320))
            self.texts['credit9'] = ('(Itens)', (560, 350))
            self.texts['credit10'] = ('opengamearts music', (360, 390))
            self.menuPage['credits'] = True

    def quitPage(self):
        """Отображение страницы выхода"""
        if not self.menuPage['quit']:
            self.clear()
            self.backgroundMenu = True
            Button(self, 365, 70, image=[self.images[11], self.images[11]], text='Quit?')
            Button(self, 365, 280, image=[self.images[10], self.images[11]], text='Yes ;-;',
                   action='pygame.event.post(pygame.event.Event(pygame.QUIT))')
            Button(self, 365, 365, image=[self.images[10], self.images[11]], text='No :)')
            self.menuPage['quit'] = True

    def difficulty(self, direction):
        """Изменение уровня сложности"""
        current_idx = self.DIFFICULTIES.index(self.difficultySelected)

        if direction == 'up':
            new_idx = (current_idx + 1) % len(self.DIFFICULTIES)
        elif direction == 'down':
            new_idx = (current_idx - 1) % len(self.DIFFICULTIES)
        else:  # return
            self.data.updateParameter('difficulty', self.difficultySelected)
            return self.difficultySelected

        self.difficultySelected = self.DIFFICULTIES[new_idx]
        return self.difficultySelected

    def load(self):
        """Загрузка игры"""
        for button in self.buttons:
            if button.clicked:
                saveGetter(self.game, button.text, loadind=True)
                self.game.gameRun(button.text)

    def run(self):
        """Основной цикл меню"""
        self.update()
        self.draw()


if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()

    menu = MainMenu()
    clock = pygame.time.Clock()

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menu.data.updateParameter('difficulty', menu.difficulty('return'))
                pygame.quit()
                quit()

        menu.run()
        pygame.display.flip()