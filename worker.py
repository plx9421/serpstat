import queue
import threading

from hint import Hint


class WorkerBase(threading.Thread):
    def __init__(self, response_queue: queue.Queue):
        super().__init__()
        self._response_queue = response_queue

    def run(self):
        while True:
            queryOne = self._response_queue.get()
            if queryOne is not None:
                self._response_queue.task_done()
                try:
                    Hint.create(
                        key=queryOne.get('hint'),
                        query=queryOne.get('query')
                    )
                except Exception as ex:
                    pass
