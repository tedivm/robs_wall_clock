import gc

print(f"Starting Free Memory: {gc.mem_free()}.")

import os

import board

import network

print(f"Modules Imported: {gc.mem_free()}.")


wifi = network.RobsNetwork(debug=True, status_neopixel=board.NEOPIXEL)
wifi.connect()

esp = wifi._wifi.esp
esp._debug = True

print(f"Network Initialized, Free Memory: {gc.mem_free()}.")


from utils.internettime import InternetTime

it = InternetTime(wifi, os.getenv("TIMEZONE", "America/Chicago"), debug=True)


MODE = os.getenv("MODE", "life_colors")
if MODE == "clock":
    from modes import clock

    clock.run(wifi, it)

elif MODE == "life":
    from modes import life_simple

    life_simple.run(wifi, it)

elif MODE == "life_colors":
    from modes import life_colors

    life_colors.run(wifi, it)
