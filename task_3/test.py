import cache_decorator
import logging
import time

def test_subsequent_calls():
    FIRST_VAL, SECOND_VAL = 0, 1
    val = FIRST_VAL
    def _func():
        return val

    func = cache_decorator.CacheDecorator(_func, 5)

    for i in range(5):
        if(func() != FIRST_VAL):
            return False

    val = SECOND_VAL
    # after 5 subsequent calls cache should reset
    if(func() != SECOND_VAL):
        return False

    return True

def test_cache_lifespan():
    FIRST_VAL, SECOND_VAL = 0, 1
    val = FIRST_VAL
    def _func():
        return val

    func = cache_decorator.CacheDecorator(_func, 10, 1)

    if(func() != FIRST_VAL):
        return False

    time.sleep(2)
    val = SECOND_VAL
    if(func() != SECOND_VAL):
        return False

    return True
def test_slow_function_short_lifespan():
    """
        If the wrapped function is slow there is a possibility that timer
        is invoked to reset the cache while the function is still executing.
        Timer would reset the newly created valid cache thinking it reset the old
        invalid cache.
    """

    FIRST_VAL, SECOND_VAL = 0, 1
    val = FIRST_VAL
    def _slow_func():
        time.sleep(5)
        return val

    slow_func = cache_decorator.CacheDecorator(_slow_func, 3, 3)
    for i in range(4):
        if(slow_func() != FIRST_VAL):
            return False

    val = SECOND_VAL
    # decorator should still be returning cached FIRST_VALUE here
    if(slow_func() != FIRST_VAL):
        return False

    return True

def test_frequent_function_long_lifespan():
    """
        If decorator does not cancel old started timers a lot of timers would
        be created when the wrapped function is frequently called thus causing
        a RuntimeError.

        This test should be run last due to a possibility of a crash.
    """
    
    def _frequent_func():
        return 0

    frequent_func = cache_decorator.CacheDecorator(_frequent_func, 5, 20)
    for i in range(100000):
        try:
            frequent_func()
        except RuntimeError:
            return False

    return True

def test_various_args():
    FIRST_VAL, SECOND_VAL = 0, 1
    val = FIRST_VAL
    def _func(*args):
        return val

    func = cache_decorator.CacheDecorator(_func)

    if(func() != FIRST_VAL):
        return False
    val = SECOND_VAL
    if(func() != FIRST_VAL):
        return False
    val = FIRST_VAL

    if(func(1, 2, 3) != FIRST_VAL):
        return False
    val = SECOND_VAL
    if(func(1, 2, 3, 5, 6) != SECOND_VAL):
        return False
    val = FIRST_VAL

    if(func([1,2,3,4]) != FIRST_VAL):
        return False
    val = SECOND_VAL
    if(func([1,2,3,4,5]) != SECOND_VAL):
        return False
    val = FIRST_VAL

    return True

TESTS = [
    test_subsequent_calls,
    test_cache_lifespan,
    test_various_args,
    test_slow_function_short_lifespan,
    test_frequent_function_long_lifespan,
]

def main():
    logging.basicConfig(format="%(levelname)s: %(message)s")

    passed_tests = 0
    for idx, test in enumerate(TESTS):
        if(not test()):
            print("Test %d: FAILED" % idx)
        else:
            passed_tests += 1
            print("Test %d: PASSED" % idx)

    print("Passed tests %d / %d" % (passed_tests, len(TESTS)))


if __name__ == '__main__':
    main()