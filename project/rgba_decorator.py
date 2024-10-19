from typing import Generator, Tuple
import itertools

TOTAL_COMBINATIONS = 256 * 256 * 256 * 51


def rgba_generator() -> Generator[Tuple[int, int, int, int], None, None]:
    """
    A generator that yields RGBA vectors where transparency (alpha)
    takes even values between 0 and 100.

    Yields:
        Tuple[int, int, int, int]: The next RGBA color in the sequence.
    """
    return (
        (r, g, b, a)
        for r in range(256)
        for g in range(256)
        for b in range(256)
        for a in range(0, 102, 2)
    )


def get_rgba_element(i: int) -> Tuple[int, int, int, int]:
    """
    Returns the i-th RGBA vector using the generator.

    Args:
        i (int): Index of the RGBA vector to retrieve.

    Returns:
        Tuple[int, int, int, int]: The RGBA color at the given index.

    Raises:
        IndexError: If the index is out of range.
    """
    if not (0 <= i < TOTAL_COMBINATIONS):
        raise IndexError("Index out of range")

    rgba_gen = rgba_generator()
    return next(itertools.islice(rgba_gen, i, i + 1))


def prime_generator() -> Generator[int, None, None]:
    """
    A generator that yields prime numbers using the Sieve of Eratosthenes method.
    This generator will continue indefinitely without a predefined limit.

    Yields:
        int: The next prime number in the sequence.
    """
    d = {}
    q = 2
    while True:
        if q not in d:
            yield q
            d[q * q] = [q]
        else:
            for p in d[q]:
                d.setdefault(p + q, []).append(p)
            del d[q]
        q += 1


def prime_decorator(func):
    """
    A decorator that takes a generator function and returns the k-th prime number.
    It optimizes performance by using a single generator instance that continues
    where it left off for sequential calls with increasing k values.

    Args:
        func (Callable): A generator function that yields prime numbers.

    Returns:
        Callable[[int], int]: A wrapped function that returns the k-th prime.
    """
    gen = None
    primes = []

    def wrapper(k: int) -> int:
        nonlocal gen

        if not isinstance(k, int):
            raise TypeError("Index must be an integer.")
        if k < 1:
            raise ValueError("Index must be a positive integer.")

        if gen is None:
            gen = func()

        if len(primes) >= k:
            return primes[k - 1]

        for prime in gen:
            primes.append(prime)
            if len(primes) == k:
                return prime

        raise ValueError("Prime number not found for the given index.")

    return wrapper


@prime_decorator
def get_prime() -> Generator[int, None, None]:
    """
    Returns a generator that yields prime numbers with a limit.

    Returns:
        Generator[int, None, None]: A prime number generator.
    """
    return prime_generator()
