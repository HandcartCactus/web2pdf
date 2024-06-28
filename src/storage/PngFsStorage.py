from web2pdf.storage.Storage import Storage


from PIL import Image


import os
import re
from datetime import datetime
from typing import List, Union


class PngFsStorage(Storage):
    def __init__(self, base_dir:str):

        if not os.path.isdir(base_dir):
            raise FileNotFoundError(base_dir)

        self.base_dir = base_dir
        self.image_files = []
        self.file_counter = 0

    def create_storage(self):
        current_time_str = re.sub('[\D]','_',datetime.now().isoformat())
        self.export_dir = os.path.join(self.base_dir, f"file_dump_{current_time_str}")
        os.mkdir(self.export_dir)

    def save_page_content(self, content:Union[List[Image.Image], Image.Image]):
        if isinstance(content, Image.Image):
            self._save_an_image(content)

        elif isinstance(content, list):
            for image in content:
                self._save_an_image(image)

        else:
            raise TypeError(f'expected PIL Image.Image, got:{type(content)}')

    def _save_an_image(self, image:Image.Image):
        self.file_counter += 1
        filename = f'page_{self.file_counter:06}.png'
        image_filepath = os.path.join(self.export_dir, filename)
        self.image_files.append(image_filepath)
        image.save(image_filepath)

    def all_content(self):
        return self.image_files

    def final_cleanup(self):
        for file in self.image_files:
            os.remove(file)
