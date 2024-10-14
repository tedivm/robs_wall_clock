import gc

print(f"Starting Free Memory: {gc.mem_free()}.")

import os
import random

import board

import network
from modes import (
    ant,
    highlife_colors,
    life_colors,
    life_simple,
    rain,
    rule30,
    war,
    wolfram_four,
    wolfram_three,
    wolfram_two,
)
from utils.gameboard import GameBoard
from utils.internettime import InternetTime
from utils.shuffle import shuffle

print(f"Modules Imported: {gc.mem_free()}.")


wifi = network.RobsNetwork(debug=True, status_neopixel=board.NEOPIXEL)
esp = wifi._wifi.esp
esp._debug = True

print(f"Network Initialized, Free Memory: {gc.mem_free()}.")

timezone = os.getenv("TIMEZONE", "America/Chicago")
clock_update = int(os.getenv("CLOCK_INTERNET_UPDATE", 3600))
disable_internet = os.getenv("DISABLE_INTERNET", "false").lower() == "true"
clock_enabled = os.getenv("CLOCK_ENABLED", "true").lower() == "true"
brightness = float(os.getenv("BRIGHTNESS", 100)) / 100.00
time_format = os.getenv("TIME_FORMAT", "24")

it = InternetTime(
    wifi,
    os.getenv("TIMEZONE", "America/Chicago"),
    debug=True,
    seconds_between_updates=clock_update,
    disable_internet=disable_internet,
)

GAMEBOARD = GameBoard(
    wifi,
    it,
    clock_enabled=clock_enabled,
    brightness=brightness,
    time_format=time_format,
)
RANDOM_EXCLUDE_MODES = ["rule30"]
MODES = {
    "ant": ant,
    "highlife_colors": highlife_colors,
    "life_colors": life_colors,
    "life_simple": life_simple,
    "rain": rain,
    "rule30": rule30,
    "war": war,
    "wolfram_two": wolfram_two,
    "wolfram_three": wolfram_three,
    "wolfram_four": wolfram_four,
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
            RANDOM_OPTIONS = list(set(MODES.keys()) - set(RANDOM_EXCLUDE_MODES))
            shuffle(RANDOM_OPTIONS)
        mode_name = RANDOM_OPTIONS.pop()
        print(f"Running {mode_name} until it finishes.")
        MODES[mode_name].run(GAMEBOARD, False)
        gc.collect()
