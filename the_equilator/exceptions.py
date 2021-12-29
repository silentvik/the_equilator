import inspect


def inspect_func(depth=1):
    current_frame = inspect.currentframe()
    caller_frame = current_frame.f_back
    for _ in range(depth-1):
        caller_frame = caller_frame.f_back
    code_obj = caller_frame.f_code
    code_obj_name = code_obj.co_name
    print("Имя вызывающего объекта: ", code_obj_name)


class EquilatorError(Exception):
    """
        Raised when can't equilate
    """
    pass
