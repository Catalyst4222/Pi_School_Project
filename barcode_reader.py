import pyzbar
from imutils.video import VideoStream
from imutils import resize

from typing import Iterator, List
from time import sleep
from random import randint

# https://www.pyimagesearch.com/2018/05/21/an-opencv-barcode-and-qr-code-scanner-with-zbar/


_IMAGE_STREAM = VideoStream(src=0).start()
# _IMAGE_STREAM = VideoStream(usePiCamera=True).start()

def _grab_frame():
    frame = _IMAGE_STREAM.read()
    frame = resize(frame, width=400)
    return frame

def _process_barcodes(frame) -> List[str]:
    """Get all barcodes from a frame
    Doesn't check yet, will do later"""
    barcodes = pyzbar.decode(frame)
    # codes = [code for code in barcodes]
    # TODO check for valid barcodes, only return the first valid
    return barcodes
    

def watch_for_barcodes() -> Iterator[str]:
    """Get infinite barcode results
    Usage: `for code in watch_for_barcodes():`"""
    while True:
        yield from get_barcode_set()


def get_barcode_set() -> Iterator[str]:
    frame = _grab_frame
    for i in _process_barcodes(frame):
        yield i


def cleanup() -> None:
    _IMAGE_STREAM.stop()
    # More?

class BarcodeReader:
    def __init__(self):
        self._stream = VideoStream(src=0).start()
        self._running = True

    def _grab_frame(self):
        frame = self._stream.read()
        frame = resize(frame, width=400)
        return frame

    def _process_barcodes(self, frame) -> List[str]:
        """Get all barcodes from a frame
        Doesn't check yet, will add later"""
        barcodes = pyzbar.decode(frame)
        # codes = [code for code in barcodes]
        # TODO check for valid barcodes, only return the first valid
        return barcodes
    
    def get_barcode_set(self) -> Iterator[str]:
        frame = self._grab_frame
        yield from self._process_barcodes(frame)

    def watch_for_barcodes(self) -> Iterator[str]:
        """Get infinite barcode results
        Usage: `for code in watch_for_barcodes():`"""
        yield from self

    def __iter__(self):
        while self._running:
            yield from self.get_barcode_set()

    def get_fake_codes(self) -> Iterator[str]:
        while self._running:
            sleep(0.5)
            num = '40000' + randint(0,9).__str__()
            yield num

    def close(self) -> None:
        self._stream.stop()
        self._running = False

    # More?