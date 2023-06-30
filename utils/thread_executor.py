import asyncio
import threading
from functools import partial
from queue import Empty, Queue
from typing import Any, Callable, Tuple, TypeVar

T = TypeVar("T")

# sourcery skip: use-contextlib-suppress
try:
    from typing_extensions import Self
except ImportError:
    pass


def set_result(future: asyncio.Future, result):
    if not future.done():
        future.set_result(result)


def resolve(future: asyncio.Future, result=None):
    loop = future.get_loop()
    loop.call_soon_threadsafe(set_result, future, result)


class AsyncThreadExecutor(threading.Thread):
    """
    A class designed to run blocking code in an async friendly way.
    New tasks are submitted to the queue, and once it is done the related future is resolved.

    Though this class can be used directly, it is recommended to subclass it.

    The intended use is as follows:

    .. code-block::

        async with ExecutorSubclass as executor:
            # replace the _submit method with your desired interface
            result = executor._submit(blocking_func, <args/kwargs>)
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._queue: Queue[Tuple[asyncio.Future, Callable[[], Any]]] = Queue()
        self._started: bool = False
        self._running: bool = False

    @property
    def started(self) -> bool:
        """If the underlying thread has been started"""
        return self._started

    @property
    def running(self) -> bool:
        """If the thread should accept more functions to call"""
        return self._running

    def _setup(self):
        """Prepare the executor"""
        # left blank for subclasses

    def run(self):
        self._started = True
        self._setup()

        while True:
            try:
                fut, func = self._queue.get(timeout=0.1)
            except Empty:
                if self._running:
                    continue
                break

            res = func()
            resolve(fut, res)

    async def close(self):
        """Shut down the executor"""
        if not self._running:
            raise ValueError("The executor has already been closed!")
        # Any cleanup here
        self._running = False

    def __await__(self):
        self.start()
        yield from ()  # need to be an iterator

    async def __aenter__(self) -> "Self":
        await self
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        # Subclasses can optionally handle errors

    async def _submit(self, func: Callable[..., T], /, *args, **kwargs) -> T:
        """Add a function to the queue and wait for it to be finished"""
        if not self.started:
            return ValueError("The executor has not been started!")

        if not self.running:
            raise ValueError("Cannot submit more functions to a closing executor!")

        part = partial(func, *args, **kwargs)
        fut = asyncio.get_running_loop().create_future()
        self._queue.put_nowait((fut, part))

        return await fut
