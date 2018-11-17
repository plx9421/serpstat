import queue
import threading
import time


class WorkerBase(threading.Thread):
    def __init__(self, wait_queue: queue.Queue, exec_queue: queue.Queue):
        super().__init__()
        self._executorQueue = exec_queue
        self._waitQueue = wait_queue

    def run(self):
        while True:
            execTime = time.time()

            countDevices = self._waitQueue.qsize()
            for i in range(countDevices):
                deviceOne = self._waitQueue.get()
                if deviceOne is not None:
                    if deviceOne.isActive:
                        self._executorQueue.put(deviceOne)
                    else:
                        self._waitQueue.put(deviceOne)
                    self._waitQueue.task_done()

            sleepTime = time.time() - execTime
            if sleepTime < 1:
                time.sleep(1 - sleepTime)
