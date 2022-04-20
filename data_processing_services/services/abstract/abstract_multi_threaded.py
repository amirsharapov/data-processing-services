from abc import ABC, abstractmethod
from threading import active_count, Thread, Lock
from time import sleep
from typing import Any, List

from .abstract import AbstractDataProcessingService


class AbstractMultiThreadedDataProcessingService(AbstractDataProcessingService, ABC):
    def __init__(self):
        super().__init__()
        self.lock = Lock()

    @abstractmethod
    def _run_in_thread(self, item: Any):
        pass

    def _run_concurrently_in_threads(self, items: List[Any], max_threads=50):
        threads = []

        for i, item in enumerate(items):
            print(f'Starting thread ... {i + 1} / {len(items)}')
            thread = Thread(target=self._run_in_thread, args=(item,), daemon=True)
            thread.start()
            threads.append(thread)

            while active_count() >= max_threads:
                sleep(1)

        for thread in threads:
            thread.join()
