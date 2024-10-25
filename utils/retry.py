import time
from functools import wraps
import logging

logger = logging.getLogger(__name__)

def retry(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        retries = 3
        delay = 2
        for attempt in range(retries):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error: {e}. Retrying...")
                time.sleep(delay)
        raise Exception("Max retries exceeded")
    return wrapper