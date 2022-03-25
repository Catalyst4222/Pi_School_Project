import multiprocessing

from receive_test import receive
from send_test import send

if __name__ == "__main__":
    # Create a pipe
    queue = multiprocessing.JoinableQueue(1)

    # Create a process to send data
    send_process = multiprocessing.Process(target=send, args=(queue,))
    send_process.start()

    # Create a process to receive data
    receive_process = multiprocessing.Process(target=receive, args=(queue,))
    receive_process.start()

    # Wait for the processes to finish
    send_process.join()
    receive_process.join()
