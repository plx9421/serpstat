import queue
import threading
import traceback
import datetime
from peewee import *

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
                except IntegrityError:
                    pass

                except Exception as ex:
                    traceback_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
                    traceback_info = ('\n--- %s: Hint.create:"%s". ---\n' %
                                      (datetime.datetime.now().isoformat(sep='z'),
                                       queryOne))
                    print(traceback_info)
                    print(traceback_lines)
