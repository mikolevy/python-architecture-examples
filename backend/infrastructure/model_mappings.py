from enum import Enum
from typing import Tuple, List, Type


def model_choices_from_enum(enum_obj: Type[Enum]) -> List[Tuple[str, str]]:
    return [(choice.name, choice.value) for choice in enum_obj]
