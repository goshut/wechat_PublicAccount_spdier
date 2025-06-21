import time
from functools import wraps


class CodeTimer:
    def __init__(self, code_name: str = None):
        self.code_name = code_name

    def __enter__(self):
        self.start_time = time.perf_counter_ns()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        duration_ns = time.perf_counter_ns() - self.start_time
        duration, unit = perf_counter_ns_change_unit(duration_ns)
        print(
            f"{self.code_name + ' ' if self.code_name else ''}运行时间为: {duration} {unit}"
        )


def calculate_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time
        print(f"函数 {func.__name__} 的运行时间为: {execution_time} 秒")
        return result

    return wrapper


def calculate_execution_time_with_format(func):
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        execution_time = end_time - start_time

        # 改进后的时间单位转换
        time_formats = [
            (1e-9, "纳秒", 1e9),
            (1e-6, "微秒", 1e6),
            (1e-3, "毫秒", 1e3),
            (1, "秒", 1),
        ]

        for threshold, unit_name, conversion in reversed(time_formats):
            if execution_time >= threshold:
                execution_time_in_unit = execution_time * conversion
                print(
                    f"函数 {func.__name__} 的运行时间为: {execution_time_in_unit:.4f} {unit_name}"
                )
                break

        return result

    return wrapper


def perf_counter_ns_change_unit(duration_ns: int):
    """改变纳秒时间单位的单位
    duration_ns: 纳秒的int值
    return:
    float: 新的数值
    str: 新的单位
    """
    if duration_ns < 1_000:
        return duration_ns, "纳秒"
    elif duration_ns < 1_000_000:
        return duration_ns / 1_000, "微秒"
    elif duration_ns < 1_000_000_000:
        return duration_ns / 1_000_000, "毫秒"
    else:
        return duration_ns / 1_000_000_000, "秒"


def print_perf_counter_ns(duration_ns):
    duration, unit = perf_counter_ns_change_unit(duration_ns)
    print(f"耗时: {duration} {unit}")


def timed(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.perf_counter_ns()  # 获取纳秒级别的当前时间
        result = func(*args, **kwargs)
        end_time = time.perf_counter_ns()
        duration_ns = end_time - start_time
        duration, unit = perf_counter_ns_change_unit(duration_ns)
        print(f"函数 {func.__name__} 的运行时间为: {duration} {unit}")

        return result

    return wrapper


# ct = CodeTimer()
