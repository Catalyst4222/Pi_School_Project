import random
import time


def receive(queue):
    while True:
        data = queue.get()
        print("|" * int(data))
        queue.task_done()

        # time.sleep(random.random())