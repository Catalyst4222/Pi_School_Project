def receive(queue):
    while True:
        data = queue.get()
        # print("|" * int(data))
        print(data)
        queue.task_done()

        # time.sleep(random.random())
