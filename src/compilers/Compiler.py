from abc import abstractmethod


class Compiler:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def compile_content(self, content):
        pass