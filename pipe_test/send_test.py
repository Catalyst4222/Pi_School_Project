import time
from multiprocessing import JoinableQueue, Pipe
from random import random

import numpy as np
import sounddevice as sd


def send(queue: JoinableQueue):

    # queue.put(b"hello")
    #
    # i = 0
    # while True:
    #     i += 1
    #     # time.sleep(random())
    #     queue.put(f"hello {i}".encode())

    def print_sound(indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        # print("|" * int(volume_norm))
        queue.put(volume_norm)

    with sd.InputStream(callback=print_sound):
        while not queue._closed:
            time.sleep(1)


def get_audio_volume(queue: JoinableQueue):
    ...
