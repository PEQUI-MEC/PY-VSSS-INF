import time


def timeToFinish(method):
    # This decorator returns time elapsed on execution of a method
    # HOW TO USE
    # Before the method, place @timeToFinish
    # In the terminal will be printed the time elapsed on method execution

    def timed(*args, **kwargs):
        tStart = time.time()
        result = method(*args, **kwargs)
        tEnd = time.time()

        print(method.__name__ + ": " + str(tEnd-tStart) + " sec")
        return result
    return timed
