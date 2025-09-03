
from datetime import datetime

def unique_slug_generator(text, separator='-'):

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    return f"{text}{separator}{timestamp}"


