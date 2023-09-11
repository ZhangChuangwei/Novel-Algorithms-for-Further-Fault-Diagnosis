from functools import wraps

# def silent_print(enable_print=True):
#     def decorator(func):
#         @wraps(func)
#         def wrapper(*args, **kwargs):
#             if enable_print:
#                 global print
#                 original_print = print
#                 print = lambda *args, **kwargs: None

#             result = func(*args, **kwargs)

#             if enable_print:
#                 print = original_print

#             return result
#         return wrapper
#     return decorator

def print_func_name(func):
    def wrapper(*args, **kwargs):
        print(f"Function name: {func.__name__}")
        return func(*args, **kwargs)
    return wrapper

