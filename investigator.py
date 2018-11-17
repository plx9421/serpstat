# coding=utf-8
import copy
import queue
import threading
import traceback
import datetime
import requests

from config import Config
from response import ResponseBase


class ExecutorBase(threading.Thread):
    def __init__(self, in_queue: queue.Queue, out_queue: queue.Queue):
        super().__init__()
        self._inQueue = in_queue
        self._outQueue = out_queue
        self._exceptionList = []

    def run(self):
        while True:
            _query = ''
            hitsOne = self._inQueue.get()
            if hitsOne:
                try:
                    # if Config.PROXY:
                    #     response = requests.get(url=(Config.BASE_URL % hitsOne),
                    #                             proxies=Config.PROXY, verify=None)
                    # else:
                    response = ResponseBase(requests.get(url=(Config.BASE_URL % hitsOne)))

                    _query = response.content.get('query', None)
                    if _query is not None:
                        self._outQueue.put({'hint': hitsOne, 'query': _query})
                        print({hitsOne: _query})

                except Exception as ex:
                    traceback_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
                    self._exceptionList.append(('\n--- %s: Hint:"%s". ---\n' %
                                                (datetime.datetime.now().isoformat(sep='z'),
                                                 hitsOne)))
                    self._exceptionList.extend(traceback_lines)

                self._inQueue.task_done()

    @property
    def exceptionList(self):
        exceptionList = copy.copy(self._exceptionList)
        self._exceptionList.clear()
        return exceptionList
