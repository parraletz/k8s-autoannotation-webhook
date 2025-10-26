from dataclasses import dataclass
from functools import lru_cache


@dataclass
class Container:
    pass


@lru_cache
def _singleton() -> Container:
    return Container()


def build_container(reset: bool = False) -> Container:
    if reset:
        return Container()
    return _singleton()
