"""Short synthesized interface and battle sounds."""

from array import array
from math import pi, sin

import pygame


class Audio:
    def __init__(self):
        self.enabled = True
        self.sounds = {}
        if not pygame.mixer.get_init():
            return
        rate = pygame.mixer.get_init()[0]
        for name, notes, duration, volume in (
            ("click", (480, 620), 0.09, 0.09),
            ("build", (330, 440, 660), 0.23, 0.12),
            ("move", (240, 330), 0.15, 0.09),
            ("hit", (113, 73, 61), 0.22, 0.17),
            ("turn", (392, 587), 0.24, 0.10),
            ("win", (262, 330, 392, 523), 0.75, 0.15),
        ):
            samples = array("h")
            length = int(rate * duration)
            for index in range(length):
                t = index / rate
                note = notes[min(len(notes) - 1, index * len(notes) // length)]
                envelope = min(1, index / (rate * 0.014)) * (1 - index / length) ** 1.65
                tone = sin(2 * pi * note * t) + 0.24 * sin(2 * pi * note * 2.01 * t)
                if name == "hit":
                    tone += 0.4 * sin(2 * pi * 4321 * t) * sin(2 * pi * 5647 * t)
                samples.append(int(28000 * volume * envelope * tone))
            self.sounds[name] = pygame.mixer.Sound(buffer=samples)

    def play(self, name):
        if self.enabled and name in self.sounds:
            self.sounds[name].play()
