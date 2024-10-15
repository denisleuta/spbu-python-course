from typing import Generator, Tuple

TOTAL_COMBINATIONS = 256 * 256 * 256 * 51


def get_rgba_element(i: int) -> Tuple[int, int, int, int]:
    """
    Returns the i-th RGBA vector by calculating its position
    without generating all combinations.

    Args:
        i (int): Index of the RGBA vector to retrieve.

    Returns:
        Tuple[int, int, int, int]: The RGBA color at the given index.

    Raises:
        IndexError: If the index is out of range.
    """
    if not (0 <= i < TOTAL_COMBINATIONS):
        raise IndexError("Index out of range")

    r = (i // (256 * 256 * 51)) % 256
    g = (i // (256 * 51)) % 256
    b = (i // 51) % 256
    a = (i % 51) * 2  # Alpha only takes even values

    return r, g, b, a


def prime_generator(limit: int = 10000) -> Generator[int, None, None]:
    """
    A generator that yields prime numbers using the Sieve of Eratosthenes method,
    with an optional limit on how many primes to calculate.

    Args:
        limit (int): The maximum number of primes to generate.

    Yields:
        int: The next prime number in the sequence, up to the limit.
    """
    D = {}
    q = 2
    count = 0  # Keep track of how many primes have been generated
    while count < limit:
        if q not in D:
            yield q  # q is prime
            D[q * q] = [q]
            count += 1
        else:
            for p in D[q]:
                D.setdefault(p + q, []).append(p)
            del D[q]
        q += 1


def prime_decorator(func):
    """
    A decorator that takes a generator function and returns the k-th prime number.

    Args:
        func (Callable): A generator function that yields prime numbers.

    Returns:
        Callable[[int], int]: A wrapped function that returns the k-th prime.
    """

    def wrapper(k: int) -> int:
        if not isinstance(k, int):  # Check if k is an integer
            raise TypeError("Index must be an integer.")
        if k < 1:  # Check if k is positive
            raise ValueError("Index must be a positive integer.")

        gen = func()
        for idx, prime in enumerate(gen, start=1):
            if idx == k:
                return prime

        raise ValueError(
            "Prime number not found for the given index."
        )  # Raise if k exceeds the number of primes

    return wrapper


@prime_decorator
def get_prime() -> Generator[int, None, None]:
    """
    Returns a generator that yields prime numbers with a limit.

    Returns:
        Generator[int, None, None]: A prime number generator.
    """
    return prime_generator(limit=1000)
