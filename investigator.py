# coding=utf-8
import queue
import threading
import traceback
import datetime
import requests

from config import Config
from response import ResponseBase


class ExecutorBase(threading.Thread):
    def __init__(self, in_queue: queue.Queue, out_queue: queue.Queue, sessions=None):
        super().__init__()
        self._inQueue = in_queue
        self._outQueue = out_queue
        self._sessions = sessions if sessions is not None else requests.session()

    def run(self):
        while True:
            hitsOne = self._inQueue.get()
            if hitsOne:
                try:
                    if Config.PROXY:
                        response = ResponseBase(self._sessions.get(url=('%s%s' % (Config.BASE_URL, hitsOne)),
                                                                   proxies=Config.PROXY, verify=False))
                    else:
                        response = ResponseBase(self._sessions.get(url=('%s%s' % (Config.BASE_URL, hitsOne)),
                                                                   timeout=300))

                    if isinstance(response.content, dict):
                        _query = response.content.get('query', [])
                    else:
                        _query = []
                    if _query is not None:
                        self._outQueue.put({'hint': hitsOne, 'query': _query})
                        # print({hitsOne: _query})

                except Exception as ex:
                    traceback_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
                    traceback_info = ('\n--- %s: ExecutorBase. Hint:"%s". ---\n' %
                                      (datetime.datetime.now().isoformat(sep='z'),
                                       hitsOne))
                    print(traceback_info)
                    print(traceback_lines)

                self._inQueue.task_done()
