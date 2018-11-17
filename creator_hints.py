import queue
import threading

from hint import Hint


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


class CreatorHintsBase(threading.Thread):
    def __init__(self, exec_queue: queue.Queue):
        super().__init__()
        self._exec_queue = exec_queue

    def run(self):
        for promt in generator_word():
            try:
                r = Hint.get(Hint.key == promt)
            except Exception as ex:
                r = ''

            if not r:
                self._exec_queue.put(promt)

