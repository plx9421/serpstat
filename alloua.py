import queue

from config import Config
from executor import ExecutorBase
from worker import WorkerBase


def generator_word():
    ALPHABET_ENG = ' abcdefghijklmnopqrstuvwxyz'
    ALPHABET_RUS = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    ALPHABET_UKR = 'абвгґдеєжзиіїйклмнопрстуфхцчшщьюя'
    ALPHABET = '%s%s%s' % (ALPHABET_ENG, ALPHABET_RUS, ALPHABET_UKR)

    for m in ALPHABET:
        for n in ALPHABET:
            for o in ALPHABET:
                _m = m if m != ' ' else ''
                _n = n if n != ' ' else ''
                _o = o if o != ' ' else ''
                yield _m + _n + _o


if __name__ == '__main__':

    executorList = []
    queueForExecute = queue.Queue()
    queueForResponse = queue.Queue()

    for i in range(Config.THREAD_COUNT):
        e = ExecutorBase(in_queue=queueForExecute,
                         out_queue=queueForResponse)
        e.daemon = True
        executorList.append(e)
        e.start()

    workerThread = WorkerBase(wait_queue=queueForResponse,
                              exec_queue=queueForExecute)
    workerThread.daemon = True
    workerThread.start()
