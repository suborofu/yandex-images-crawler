import hashlib
import io
import logging
from multiprocessing import Queue, Value, get_logger
from pathlib import Path
from typing import FrozenSet, Tuple, Union

import numpy as np
import requests
from PIL import Image

requests.packages.urllib3.disable_warnings()


class ImageLoader:
    def __init__(
        self,
        load_queue: Queue,
        image_size: Tuple[int, int],
        image_dir: Union[str, Path],
        skip_files: FrozenSet[str] = frozenset(),
        is_active=Value("i", True),
    ):
        self.load_queue: Queue = load_queue
        self.min_width: int = image_size[0]
        self.min_height: int = image_size[1]
        self.image_dir: Path = Path(image_dir)
        self.skip_files: set[str] = skip_files
        self.is_active = is_active

        self.headers: dict[str, str] = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Referer": "https://yandex.com/",
        }

        self.logger: logging.Logger = get_logger()
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s - %(asctime)s - %(message)s"))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def run(self):
        while True:
            if not self.is_active.value:
                return

            link, (width, height) = self.load_queue.get()

            if width is None or height is None or (width >= self.min_width and height >= self.min_height):
                self.logger.info(link)
                try:
                    response = requests.get(link, headers=self.headers, verify=False, timeout=10)
                except:
                    continue
                if 200 <= response.status_code < 300:
                    try:
                        img = Image.open(io.BytesIO(response.content))
                    except:
                        continue

                    width, height = img.size
                    hash_name = hashlib.sha256(np.array(img)).hexdigest()

                    img_path = self.image_dir / (hash_name + ".png")

                    if (
                        hash_name not in self.skip_files
                        and not img_path.exists()
                        and width >= self.min_width
                        and height >= self.min_height
                    ):
                        img.save(img_path, "PNG")
