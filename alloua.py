import queue
import time

import requests
from requests.adapters import HTTPAdapter

from config import Config
from creator_hints import CreatorHintsBase
from hint import Hint
from investigator import ExecutorBase
from worker import WorkerBase

if __name__ == '__main__':
    hs = requests.session()
    ha = HTTPAdapter(
        pool_connections=1,
        pool_maxsize=Config.THREAD_COUNT,
        max_retries=5
    )
    hs.mount('https://', ha)
    hs.mount('http://', ha)

    Hint.create_table()

    queueForExecute = queue.Queue()
    queueForResponse = queue.Queue()

    creatorHints = CreatorHintsBase(exec_queue=queueForExecute)
    creatorHints.daemon = True
    creatorHints.start()

    for i in range(Config.THREAD_COUNT):
        e = ExecutorBase(in_queue=queueForExecute,
                         out_queue=queueForResponse,
                         sessions=hs)
        e.daemon = True
        e.start()

    workerThread = WorkerBase(response_queue=queueForResponse)
    workerThread.daemon = True
    workerThread.start()

    creatorHints.join()

    while True:
        time.sleep(10)
        if queueForExecute.empty() and queueForResponse.empty():
            break

    print('Finita la comedia')
