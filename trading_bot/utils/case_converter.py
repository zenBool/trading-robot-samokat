import re


def camel_case_to_snake_case(input_str: str) -> str:
    """
    >>> camel_case_to_snake_case("SomeSDK")
    'some_sdk'
    >>> camel_case_to_snake_case("RServoDrive")
    'r_servo_drive'
    >>> camel_case_to_snake_case("SDKDemo")
    'sdk_demo'
    >>> camel_case_to_snake_case("File")
    'files'
    >>> camel_case_to_snake_case("test")
    'tests'
    >>> camel_case_to_snake_case("tRest")
    'trests'
    """

    if sum(1 for c in input_str if c.isupper()) > 1:
        input_str = re.sub("([a-z])([A-Z])", r"\1_\2", input_str)
        input_str = re.sub("([A-Z])([A-Z][a-z])", r"\1_\2", input_str)
    else:
        return input_str.lower() + "s"

    # Первое преобразование добавляет подчеркивание перед каждой заглавной буквой, кроме первой.
    # input_str = re.sub(r"(?<!^)(?=[A-Z][a-z])", "_", input_str)
    # Второе преобразование добавляет подчеркивание перед последовательностями заглавных букв, если за ними следует строчная буква.
    # input_str = re.sub(r"(?<=[a-z])(?=[A-Z])", "_", input_str)

    #  Оба варианта рабочие

    return input_str.lower()
