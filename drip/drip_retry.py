from requests.exceptions import RequestException
from retry import retry

from drip import DripPy


class DripPyRetry(object):
    """
    A wrapper class that provides retry functionality to the DripPy main class
    We recommend using this over using DripPy directly
    """
    def __init__(self, token, account_id):
        self.drip_py = DripPy(token, account_id)

    def __getattr__(self, item):
        func = self.drip_py.__getattribute__(item)

        @retry((RequestException, ), tries=3, delay=1, backoff=2)
        def retry_func(*args, **kwargs):
            return func(*args, **kwargs)
        return retry_func
