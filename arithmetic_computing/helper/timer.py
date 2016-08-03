import time


class Timer(object):
    """Small timer helper to get time in seconds between start and now
    """

    def __init__(self):
        self._start = None

    def start(self):
        """Start the timer
        """
        self._start = self._get_current_time()

    def reset(self):
        """Reset the timer
        """
        self._start = None

    def time(self):
        """Return the time elapsed between the start of the timer and now

        :return: Time elapsed in seconds
        :rtype: float
        """
        if self._start is None:
            # Timer hasn't been started
            return float(0)

        actual = self._get_current_time()
        # Use float to have  more precision than the second
        return float(actual - self._start) / 1000

    def _get_current_time(self):
        """Get the current time
        :return: Current time
        :rtype: int
        """
        return int(round(time.time() * 1000))
