import pygame
from pygame import mixer
from numpy import random
from randomizer import Randomizer

pygame.init()

screen = pygame.display.set_mode((800, 600))
mixer.init()
mixer.music.set_volume(1)


class Button:
    def __init__(
        self,
        fontSize,
        textColor,
        color,
        colorWhenMouseOver,
        colorWhenClicked,
        pos,
        width,
        height,
        onClick,
        text="",
    ):
        self.color = color
        self.fontSize = fontSize
        self.textColor = textColor
        self.defaultColor = color
        self.colorWhenMouseOver = colorWhenMouseOver
        self.colorWhenClicked = colorWhenClicked
        self.pos_uncentered = pos
        self.pos = [pos[0] - width / 2, pos[1] - height / 2]
        self.x = self.pos[0]
        self.y = self.pos[1]
        self.width = width
        self.height = height
        self.onCLick = onClick
        self.text = text
        self.clicked = False

    def draw(self, win, outline=None):
        self.x = self.pos[0]
        self.y = self.pos[1]
        # Call this method to draw the Button on the screen
        if outline:
            pygame.draw.rect(
                win,
                outline,
                (self.x - 2, self.y - 2, self.width + 4, self.height + 4),
                0,
            )

        pygame.draw.rect(
            win,
            self.color,
            (int(self.x), int(self.y), int(self.width), int(self.height)),
            0,
        )

        if self.text != "":
            font = pygame.font.Font("freesansbold.ttf", self.fontSize)
            text = font.render(self.text, True, self.textColor)
            win.blit(
                text,
                (
                    int(self.x + (self.width / 2 - text.get_width() / 2)),
                    int(self.y + (self.height / 2 - text.get_height() / 2)),
                ),
            )

        if self.onCLick != "":
            if self.isOver(pygame.mouse.get_pos()):
                if pygame.mouse.get_pressed()[0]:
                    if not self.clicked:
                        self.clicked = True
                        self.color = self.colorWhenClicked
                        eval(self.onCLick)
                else:
                    self.clicked = False
                    self.color = self.colorWhenMouseOver
            else:
                self.clicked = False
                self.color = self.defaultColor

    def isOver(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True

        return False


class SongEntry:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.unplayed_color = (100, 100, 100)
        self.played_color = (50, 50, 50)
        self.playing_color = (150, 150, 150)
        self.color = self.unplayed_color
        self.playing = False

    def draw(self, win, pos, size):
        if self.playing:
            self.color = self.playing_color
        pygame.draw.rect(
            win,
            self.color,
            (pos[0], pos[1], size[0], size[1]),
            0,
        )
        font = pygame.font.Font("freesansbold.ttf", 20)
        text = font.render(self.name, True, (255, 255, 255))
        win.blit(
            text,
            (
                int(pos[0] + (size[0] / 2 - text.get_width() / 2)),
                int(pos[1] + (size[1] / 2 - text.get_height() / 2)),
            ),
        )


class SongDisplay:
    def __init__(self):
        self.song_list = [SongEntry(str(i + 1) + ".mp3", i + 1) for i in range(20)]
        self.playing = -1
        self.prev_playing = -1

    def draw(self, win):
        for i, song_entry in zip(range(len(self.song_list)), self.song_list):
            song_entry.draw(win, (600, 30 * i), (200, 30))
        if self.playing != -1 and self.playing != self.prev_playing:
            self.song_list[self.playing].playing = True
            if self.prev_playing != -1:
                self.song_list[self.prev_playing].playing = False
            self.prev_playing = self.playing


play_button = Button(
    25,
    (255, 255, 255),
    (50, 150, 30),
    (75, 170, 40),
    (120, 255, 90),
    [400, 450],
    100,
    50,
    "play_or_pause()",
    "Play",
)

next_button = Button(
    25,
    (255, 255, 255),
    (50, 150, 30),
    (75, 170, 40),
    (120, 255, 90),
    [200, 450],
    100,
    50,
    "play_next(song_display)",
    "Next",
)

song_randomizer = Randomizer()


def play_next(song_display):
    global song_randomizer
    global play_button
    if song_randomizer.paused:
        mixer.music.unpause()
        song_randomizer.paused = False
        play_button.text = "Pause"
    song_display.playing = song_randomizer.play_next()
    # print(song_list[song_no - 1])


def play_or_pause():
    global song_randomizer
    global play_button
    if song_randomizer.paused:
        mixer.music.unpause()
        song_randomizer.paused = False
        play_button.text = "Pause"
    else:
        mixer.music.pause()
        song_randomizer.paused = True
        play_button.text = "Play"


# song_list = [i + 1 for i in range(20)]
song_display = SongDisplay()
running = True

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_n:
                play_next(song_display)
                # print(len(song_list))

    if not mixer.music.get_busy() and not song_randomizer.paused:
        play_next(song_display)

    for song in song_display.song_list:
        if song.number in song_randomizer.song_list:
            song.color = song.unplayed_color
        else:
            song.color = song.played_color

    if song_display.playing != -1:
        font = pygame.font.Font("freesansbold.ttf", 40)
        font2 = pygame.font.Font("freesansbold.ttf", 80)
        text1 = font.render(
            "Now Playing:",
            True,
            (255, 255, 255),
        )
        text2 = font2.render(
            str(song_display.playing + 1) + ".mp3", True, (255, 255, 255)
        )
        screen.blit(text1, (170, 100))
        screen.blit(text2, (170, 240))

    keys = pygame.key.get_pressed()
    play_button.draw(screen, (20, 90, 10))
    next_button.draw(screen, (20, 90, 10))
    song_display.draw(screen)
    pygame.display.update()
