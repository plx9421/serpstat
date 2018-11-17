import queue

from config import Config
from creator_hints import CreatorHintsBase
from hint import Hint
from investigator import ExecutorBase
from worker import WorkerBase

if __name__ == '__main__':
    Hint.create_table()

    executorList = []
    queueForExecute = queue.Queue()
    queueForResponse = queue.Queue()

    creatorHints = CreatorHintsBase(exec_queue=queueForExecute)
    creatorHints.daemon = True
    creatorHints.start()

    for i in range(Config.THREAD_COUNT):
        e = ExecutorBase(in_queue=queueForExecute,
                         out_queue=queueForResponse)
        e.daemon = True
        executorList.append(e)
        e.start()

    workerThread = WorkerBase(response_queue=queueForResponse)
    workerThread.daemon = True
    workerThread.start()

    workerThread.join(10)

    print()
