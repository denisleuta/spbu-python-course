import time
import pytest
import sys
import os
from typing import Tuple

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.thread_pool import ThreadPool


def test_enqueue_and_execution():
    pool = ThreadPool(num_threads=3)

    tasks_executed = []

    def task(id):
        tasks_executed.append(id)

    for i in range(5):
        pool.enqueue(lambda i=i: task(i))

    time.sleep(1)
    pool.dispose()

    assert len(tasks_executed) == 5


def test_dispose_allows_completion():
    pool = ThreadPool(num_threads=2)

    def long_task():
        time.sleep(2)

    pool.enqueue(long_task)
    pool.enqueue(long_task)

    time.sleep(0.5)
    pool.dispose()

    assert all(not thread.is_alive() for thread in pool.threads)


def test_minimum_threads():
    pool = ThreadPool(num_threads=4)
    assert len(pool.threads) >= 4
    pool.dispose()


@pytest.mark.timeout(54)
def test_thread_pool_works_with_timeout():
    pool = ThreadPool(num_threads=3)

    def example_task():
        time.sleep(0.1)

    for _ in range(10):
        pool.enqueue(example_task)

    pool.dispose()
