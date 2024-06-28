from abc import abstractmethod


class Storage:
    def __init__(self) -> None:
        pass

    @abstractmethod
    def create_storage(self):
        pass

    @abstractmethod
    def save_page_content(self, content):
        pass

    @abstractmethod
    def all_content(self):
        pass