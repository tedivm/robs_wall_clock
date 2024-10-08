import time
import board
import random

from rainbowio import colorwheel
from adafruit_matrixportal.matrixportal import MatrixPortal

from utils.memory import logged_gc

def run(network, it):

    matrixportal = MatrixPortal(
        status_neopixel=board.NEOPIXEL,
        debug=True,
        esp=network._wifi.esp,
        use_wifi=False,
        bit_depth=4,
    )
    matrixportal.network = network

    scale_factor = 2
    iteration = random.randint(0, 255)

    matrixportal.add_text(
        text_position=(
            (matrixportal.graphics.display.width // 2) - ((14 * scale_factor) + 1),
            (matrixportal.graphics.display.height // 2),
        ),
        text_color=colorwheel(iteration),
        text_scale=scale_factor,
    )

    old_text = ""
    while True:
        current_time = it.get_time()

        # Only update the time if it has changed, to avoid flickering.
        new_text = f"{current_time.hour:02}:{current_time.minute:02}"

        if new_text != old_text:
            # GC collect before to ensure space for the buffers.
            color = colorwheel(iteration)
            print(f"Iteration: {iteration}, Color: {color}")
            matrixportal.set_text_color(color, 0)
            logged_gc()
            matrixportal.set_text(new_text, 0)
            iteration += 1
            if iteration > 255:
                iteration = 0
            logged_gc()

            old_text = new_text

        time.sleep(1)
        # GC collect after to clean up.
        logged_gc(log=False)
