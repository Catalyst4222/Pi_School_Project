import time
from multiprocessing import JoinableQueue

import numpy as np
import sounddevice as sd


def send(queue: JoinableQueue):


    def print_sound(indata, *_):
        volume_norm = np.linalg.norm(indata) * 10
        queue.put(volume_norm)

    with sd.InputStream(callback=print_sound):
        # noinspection PyUnresolvedReferences,PyProtectedMember
        while not queue._closed:
            time.sleep(1)


