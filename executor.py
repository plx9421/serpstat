# coding=utf-8
import copy
import queue
import threading
import traceback
import datetime


class ExecutorBase(threading.Thread):
    def __init__(self, in_queue: queue.Queue, out_queue: queue.Queue):
        super().__init__()
        self._inQueue = in_queue
        self._outQueue = out_queue
        self._exceptionList = []

    def run(self):
        while True:
            deviceOne = self._inQueue.get()
            if deviceOne is not None:
                try:
                    deviceOne.Execute()
                except Exception as ex:
                    traceback_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
                    self._exceptionList.append(('\n--- %s: Group:%s. Device Serial:%s ---\n' %
                                                 (datetime.datetime.now().isoformat(sep='z'),
                                                  deviceOne.deviceHeader.groupName,
                                                  deviceOne.deviceSerial)))
                    self._exceptionList.extend(traceback_lines)

                self._inQueue.task_done()
                self._outQueue.put(deviceOne)

    @property
    def exceptionList(self):
        exceptionList = copy.copy(self._exceptionList)
        self._exceptionList.clear()
        return exceptionList
