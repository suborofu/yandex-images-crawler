import logging
import os
from multiprocessing import Value, get_logger
from pathlib import Path
from typing import Union
import time


class CountChecker:
    def __init__(self, image_dir: Union[Path, str], image_count: int, is_active: Value = Value("i", True)):
        self.image_dir = image_dir
        self.image_count = image_count
        self.is_active = is_active

        self.logger = get_logger()
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.INFO)

    def run(self):
        while True:
            if not self.is_active.value:
                return
            for _, _, files in os.walk(self.image_dir):
                if len(files) >= self.image_count:
                    self.logger.info("The required number of images is reached.")
                    self.is_active.value = False
                break
            time.sleep(1)
