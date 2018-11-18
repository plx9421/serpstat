import queue
import time

import requests
from requests.adapters import HTTPAdapter

from config import Config
from creator_hints import CreatorHintsBase
from hint import Hint
from investigator import investigatorBase
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

    investigatorThreadList = []
    queueForExecute = queue.Queue()
    queueForResponse = queue.Queue()

    creatorHintsThread = CreatorHintsBase(exec_queue=queueForExecute)
    creatorHintsThread.daemon = True
    creatorHintsThread.start()

    for i in range(Config.THREAD_COUNT):
        investigatorThread = investigatorBase(in_queue=queueForExecute,
                                              out_queue=queueForResponse,
                                              sessions=hs)
        investigatorThreadList.append(investigatorThread)
        investigatorThread.daemon = True
        investigatorThread.start()

    workerThread = WorkerBase(response_queue=queueForResponse)
    workerThread.daemon = True
    workerThread.start()

    creatorHintsThread.join()

    while True:
        time.sleep(10)
        if queueForExecute.empty() and queueForResponse.empty():
            break

        for i in investigatorThreadList:
            if i.isAlive(): continue
        else:
            print('All Treads are stoped')
            break

    print('Finita la comedia')
