import threading


def thread(func):
    def inner(*args, **kwargs):
        threading.Thread(target=lambda: func(*args, **kwargs), daemon=True).start()

    return inner
