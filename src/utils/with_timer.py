import time


def with_timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time() - start
        print(f"Function {func.__name__} took {end:.4f} seconds")
        return result

    return wrapper
