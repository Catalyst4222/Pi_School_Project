"""
A group of functions to manage audio
"""
import multiprocessing
from typing import Optional

import numpy as np
import sounddevice as sd


class _Volume(multiprocessing.Process):
    """
    A class to manage the volume of the audio
    """

    def __init__(self):
        super().__init__()
        self.volume: float = 0
        self.queue: multiprocessing.Queue = multiprocessing.JoinableQueue(10)  # restrict size

    def run(self):
        sd.InputStream(callback=self.set_volume).start()

    def set_volume(self, indata, frames, time, status):
        volume_norm = np.linalg.norm(indata) * 10
        # print("|" * int(volume_norm))
        self.volume = volume_norm

        if self.queue.full():  # prevent overflow
            self.queue.get()

        self.queue.put(volume_norm)
        print('audio volume:', volume_norm)


    def get_volume(self) -> float:
        return self.volume


_VOLUME: _Volume = _Volume()


def volume_queue():
    """
    Get a queue that will be updated with volumes every so often

    :return: a queue full of volumes
    :rtype: multiprocessing.Queue
    """
    return _VOLUME.queue


def get_volume():
    """
    Get the current volume

    :return: The volume
    :rtype: float
    """
    return _VOLUME.volume
