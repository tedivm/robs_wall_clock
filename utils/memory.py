import gc

def gc_decorator(func):
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        logged_gc(func.__name__)
        return res
    return wrapper

def logged_gc(source="", log=True):
    gc.collect()
    if not log:
        return
    if source:
        print(f"{source}: Garbage Collected, Free memory at: {gc.mem_free()}.")
    else:
        print(f"Garbage Collected, Free memory at: {gc.mem_free()}.")
