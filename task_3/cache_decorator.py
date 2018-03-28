import logging
import threading
import time

class CacheDecorator:
    __MIN_MAX_SUBSEQUENT_CALLS = 2
    __MIN_CACHE_LIFESPAN = 1

    def __init__(self, func, max_subsequent_calls=10, cache_lifespan=300):
        self.__max_subsequent_calls = int(max_subsequent_calls)
        if(self.__max_subsequent_calls < 2):
            logging.warning("Clamping max_subsequent_calls to %d" 
                            % self.__MIN_MAX_SUBSEQUENT_CALLS)
            self.__max_subsequent_calls = self.__MIN_MAX_SUBSEQUENT_CALLS

        self.__cache_lifespan = cache_lifespan
        if(self.__cache_lifespan < self.__MIN_CACHE_LIFESPAN):
            logging.warning("Clamping cache lifespan to %d"
                            % self.__MIN_CACHE_LIFESPAN)
            self.__cache_lifespan = self.__MIN_CACHE_LIFESPAN

        self.__lock = threading.Lock()
        self.__n_subsequent_calls = 0
        self.__timer = None
        self.__args = None
        self.__kwargs = None
        self.__value = None
        self.__func = func

    def __del__(self):
        if(self.__timer):
            self.__timer.cancel()

    def __reset_cache(self):
        with self.__lock:
            timer_running_for = time.time() - self.__timer_started_at
            if(timer_running_for >= self.__cache_lifespan):
                logging.debug("Cache lifespan expired, resetting...")
                self.__n_subsequent_calls = 0
                self.__args = None
                self.__kwargs = None
                self.__value = None

    def __start_new_timer(self):
        if(self.__timer):
            # cancel old timer to keep number of spawned threads constant
            self.__timer.cancel()
        # need to save timestamp when last timer was started in case
        # of a lot of quick subsequent calls to a very slow wrapped function
        # (an old timer could try resetting the cache while the main thread 
        # is executing the wrapped function thus the timer cannot be cancelled anymore)
        self.__timer_started_at = time.time()
        self.__timer = threading.Timer(self.__cache_lifespan, self.__reset_cache)
        self.__timer.start()

    def __call__(self, *args, **kwargs):
        logging.debug("Function called with:\n\targs = %s\n\tkwargs = %s"
                         % (args, kwargs))
        with self.__lock:
            logging.debug("Cached arguments are:\n\targs = %s\n\tkwargs = %s"
                             % (self.__args, self.__kwargs))

            if(self.__n_subsequent_calls < self.__max_subsequent_calls and
                    self.__args == args and
                    self.__kwargs == kwargs):
                self.__n_subsequent_calls += 1
                logging.debug("Returning cached value:\n\tcache = %s\n\tsubsequent calls = %d"
                                 % (self.__value, self.__n_subsequent_calls))
            else:
                logging.debug("Calling wrapped function...")
                self.__args = args
                self.__kwargs = kwargs
                self.__value = self.__func(*args, **kwargs)
                self.__n_subsequent_calls = 1
                self.__start_new_timer()

            return self.__value