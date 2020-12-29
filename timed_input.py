import msvcrt
import sys
import time


class TimeoutExpired(Exception):
    pass


def __input_with_timeout(prompt, timeout, timer=time.monotonic):
    """ Private function """
    sys.stdout.write(prompt)
    sys.stdout.flush()
    endtime = timer() + timeout

    # waits for a key to be pressed within the time given (in seconds)
    # If time expires, pass
    while timer() < endtime:
        if msvcrt.kbhit():
            result = input()
            return result
        time.sleep(0.04)
    raise TimeoutExpired


def timed_input(prompt='', timer=10):
    """
    Importable function that accepts a prompt and a time (in seconds)
    This function waits for an input and returns an empty string if a TimeoutExpired exception is raised.
    If an input is made before the set timer expires, the function returns the input"""

    try:
        answer = __input_with_timeout(prompt, timer)
    except TimeoutExpired:
        return ''
    else:
        return answer
