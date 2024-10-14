import gc
import os

LOG_MEMORY = os.getenv("LOG_MEMORY", "False").lower() == "true"


def gc_decorator(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        logged_gc(func.__name__)
        return res

    return wrapper


def logged_gc(source="", log=True, log_always=False):
    gc.collect()
    if not log_always:
        if not log or not LOG_MEMORY:
            return
    if source:
        print(f"{source}: Garbage Collected, Free memory at: {gc.mem_free()}.")
    else:
        print(f"Garbage Collected, Free memory at: {gc.mem_free()}.")
