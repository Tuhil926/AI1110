from pygame import mixer
from numpy import random


class Randomizer:
    def __init__(self):
        self.song_list = [i + 1 for i in range(20)]
        self.paused = True

    def play_next(self):
        if len(self.song_list) == 0:
            for i in range(20):
                self.song_list.append(i + 1)
        song_no = random.randint(1, len(self.song_list) + 1)
        mixer.music.stop()
        mixer.music.load("songs/" + str(self.song_list[song_no - 1]) + ".mp3")
        mixer.music.play()
        # print(song_list[song_no - 1])
        return self.song_list.pop(song_no - 1) - 1
