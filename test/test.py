# import time
# import functools

# def async_timer(func):
#     """Декоратор для вимірювання часу виконання асинхронної функції"""
#     @functools.wraps(func)
#     async def wrapper(*args, **kwargs):
#         start = time.perf_counter()
#         result = await func(*args, **kwargs)
#         end = time.perf_counter()
#         print(f"Функція {func.__name__} виконана за {end - start:.4f} секунд")
#         return result
#     return wrapper
