import queue
import threading
import traceback
import datetime
from peewee import *

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
                Hint.get(Hint.key == promt)
            except DoesNotExist:
                self._exec_queue.put(promt)
            except IntegrityError:
                pass
            except Exception as ex:
                traceback_lines = traceback.format_exception(ex.__class__, ex, ex.__traceback__)
                traceback_info = ('\n--- %s: CreatorHintsBase.Hint.key == :"%s". ---\n' %
                                  (datetime.datetime.now().isoformat(sep='z'),
                                   promt))
                print(traceback_info)
                print(traceback_lines)
