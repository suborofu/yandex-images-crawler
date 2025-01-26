import logging
import os
from multiprocessing import Value, get_logger
from pathlib import Path
from typing import Union
import time


class CountChecker:
    def __init__(
        self, image_dir: Union[Path, str], image_count: int, is_active=Value("i", True)
    ):
        self.image_dir: Path = Path(image_dir)
        self.image_count: int = image_count
        self.is_active = is_active

        self.logger: logging.Logger = get_logger()
        handler = logging.StreamHandler()
        handler.setFormatter(
            logging.Formatter("%(levelname)s - %(asctime)s - %(message)s")
        )
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def run(self):
        while True:
            if not self.is_active.value:
                return
            for _, _, files in os.walk(self.image_dir):
                if len(files) >= self.image_count and self.image_count > 0:
                    self.logger.info("The required number of images is reached.")
                    self.is_active.value = False
                break
            time.sleep(1)
