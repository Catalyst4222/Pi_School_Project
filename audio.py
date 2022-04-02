"""
A group of functions to manage audio
This is an awful mess
"""
import audioop
import threading
import time
import wave
from collections import deque
from math import log10
from threading import Condition

import numpy as np
import pyaudio
from numpy import average

_CHUNK = 1024
_FORMAT = pyaudio.paInt16
_CHANNELS = 1
_RATE = 12800
_RECORD_SECONDS = 5

_VOLUMES = 0
_SET_VOLUME = False
_THING = Condition()


# decibel = 20 * log10(rms)
def _callback(in_data, frame_count, time_info, status):
    global _VOLUMES, _SET_VOLUME

    print(threading.current_thread())

    if _SET_VOLUME:
        with _THING:
            _VOLUMES = 20 * log10(audioop.rms(in_data, 2))
            _THING.notify_all()

    _SET_VOLUME = False

    # print(np.linalg.norm(_VOLUMES))
    return None, pyaudio.paContinue


p = pyaudio.PyAudio()

stream = p.open(
    format=_FORMAT,
    channels=_CHANNELS,
    rate=_RATE,
    input=True,
    frames_per_buffer=_CHUNK,
    stream_callback=_callback,
)


def get_volume():
    global _SET_VOLUME

    _SET_VOLUME = True
    with _THING:
        _THING.wait()
        return _VOLUMES


def stop():
    """warning: will stop all audio sources using it"""
    stream.stop_stream()
    stream.close()
    p.terminate()
