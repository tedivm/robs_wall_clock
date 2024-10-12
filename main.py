import gc

print(f"Starting Free Memory: {gc.mem_free()}.")

import os
import random

import board

import network
from modes import highlife_colors, life_colors, life_simple, rain, war
from utils.gameboard import GameBoard
from utils.internettime import InternetTime

print(f"Modules Imported: {gc.mem_free()}.")


def shuffle(lst):
    for i in range(len(lst)):
        j = random.randrange(0, len(lst))
        lst[i], lst[j] = lst[j], lst[i]


wifi = network.RobsNetwork(debug=True, status_neopixel=board.NEOPIXEL)
esp = wifi._wifi.esp
esp._debug = True

print(f"Network Initialized, Free Memory: {gc.mem_free()}.")


it = InternetTime(wifi, os.getenv("TIMEZONE", "America/Chicago"), debug=True)


GAMEBOARD = GameBoard(wifi, it)

MODES = {
    "life_simple": life_simple,
    "life_colors": life_colors,
    "war": war,
    "rain": rain,
    "highlife_colors": highlife_colors,
}

run_forever = False
mode_name = os.getenv("MODE", False)

if mode_name:
    if mode_name in MODES:
        MODE = MODES[mode_name]
        run_forever = True
    else:
        print(f"Mode {mode_name} not found, running random modes.")

RANDOM_OPTIONS = []
while True:
    if run_forever:
        print(f"Running {mode_name} forever.")
        MODE.run(GAMEBOARD, True)
    else:
        if not RANDOM_OPTIONS:
            RANDOM_OPTIONS = list(MODES.keys())
            shuffle(RANDOM_OPTIONS)
        mode_name = RANDOM_OPTIONS.pop()
        print(f"Running {mode_name} until it finishes.")
        MODES[mode_name].run(GAMEBOARD, False)
        gc.collect()
