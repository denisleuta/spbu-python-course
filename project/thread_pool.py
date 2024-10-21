import threading
import concurrent.futures
import itertools
from typing import List, Callable, Tuple


class ThreadPool:
    def __init__(self, num_threads: int) -> None:
        """
        Initializes the thread pool with a specified number of threads.

        :param num_threads: Number of threads in the pool.
        """
        self.num_threads = num_threads
        self.tasks = []
        self.threads = []
        self.lock = threading.Lock()
        self.condition = threading.Condition(self.lock)
        self._shutdown = False

        # Start worker threads
        for _ in range(self.num_threads):
            thread = threading.Thread(target=self._worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def _worker(self) -> None:
        """
        Worker method that runs in each thread. Waits for tasks and executes them.
        """
        while True:
            with self.condition:
                while not self.tasks and not self._shutdown:
                    self.condition.wait()
                if self._shutdown and not self.tasks:
                    break
                task = self.tasks.pop(0)
            task()

    def enqueue(self, task: Callable[[], None]) -> None:
        """
        Adds a task to the queue. The task will be executed by an available thread.

        :param task: A function to be executed by the thread pool.
        """
        with self.condition:
            if not self._shutdown:
                self.tasks.append(task)
                self.condition.notify()

    def dispose(self) -> None:
        """
        Shuts down the thread pool. It waits for all current tasks to complete,
        but no new tasks will be accepted.
        """
        with self.condition:
            self._shutdown = True
            self.condition.notify_all()

        # Wait for all threads to complete
        for thread in self.threads:
            thread.join()


def sum_cartesian_product(sets: List[List[int]]) -> int:
    """
    Computes the sum of the full Cartesian product of integer sets in parallel.

    :param sets: A list of integer sets for the Cartesian product.
    :return: The sum of all elements in the Cartesian product.
    """
    # Generate the full Cartesian product
    cartesian_product = itertools.product(*sets)

    # Function to sum a combination of integers
    def sum_combination(combination: Tuple[int]) -> int:
        return sum(combination)

    total_sum = 0
    # Parallel summation
    with concurrent.futures.ThreadPoolExecutor() as executor:
        # Map each combination to the summing function and gather results
        results = list(executor.map(sum_combination, cartesian_product))

    # Compute the total sum
    total_sum = sum(results)
    return total_sum
