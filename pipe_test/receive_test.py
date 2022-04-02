def receive(queue):
    while True:
        data = queue.get()
        print(data)
        queue.task_done()

