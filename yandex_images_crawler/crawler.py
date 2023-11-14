import hashlib
import logging
import time
from pathlib import Path
from typing import List, Tuple, Union

import numpy as np
import requests
from PIL import Image
from selenium import webdriver
from selenium.webdriver.common.by import By

requests.packages.urllib3.disable_warnings()


class YandexCrawler:
    def __init__(
        self,
        link: str,
        image_size: Tuple[int, int],
        image_dir: Union[str, Path],
        previous_images: List[Union[str, Path]] = [],
        id=0,
    ):
        self.image_dir = Path(image_dir)
        self.image_dir.mkdir(parents=True, exist_ok=True)
        self.temp_file = Path(__file__).parent / f"temp{id}"
        self.start_link = link
        self.id = str(id)
        self.driver = webdriver.Firefox()
        self.min_width, self.min_height = image_size
        self.files = previous_images
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Referer": "https://yandex.com/",
        }

    def get_image(self):
        width, height = None, None
        try:
            width, height = [
                int(i)
                for i in self.driver.find_element(
                    By.CSS_SELECTOR, "span[class*='OpenImageButton-RightText']"
                ).text.split("×")
            ]
        except:
            for elem in self.driver.find_elements(
                By.CSS_SELECTOR, "span[class*='Button2-Text']"
            ):
                try:
                    width, height = [int(i) for i in elem.text.split("×")]
                    break
                except:
                    pass

        if (
            width is None
            or height is None
            or (width >= self.min_width and height >= self.min_height)
        ):
            link = self.driver.find_element(
                By.CLASS_NAME, "MMImage-Origin"
            ).get_attribute("src")
            if "avatars.mds.yandex.net" in link or "yandex-images" in link:
                time.sleep(10)
                link = self.driver.find_element(
                    By.CLASS_NAME, "MMImage-Origin"
                ).get_attribute("src")
                if "avatars.mds.yandex.net" in link or "yandex-images" in link:
                    return

            data = requests.get(link, headers=self.headers, verify=False, timeout=15)
            if 200 <= data.status_code < 300:
                with open(self.temp_file, "wb") as f:
                    for chunk in data:
                        f.write(chunk)

                try:
                    img = Image.open(self.temp_file)
                except:
                    return

                width, height = img.size
                new_name = hashlib.sha256(np.array(img)).hexdigest() + ".png"

                if (
                    new_name not in self.files
                    and width >= self.min_width
                    and height >= self.min_height
                ):
                    img.save(self.image_dir / new_name, "PNG")
                    self.files.append(new_name)

    def next(self):
        try:
            btn = self.driver.find_element(
                By.CSS_SELECTOR, "div[class*='CircleButton_type_next']"
            )
            btn.click()
        except:
            logging.critical(f"Process #{self.id} can't move to the next image.")

    def run(self):
        self.driver.get(self.start_link)
        while True:
            try:
                self.get_image()
                self.next()
            except Exception as e:
                logging.critical(e)
                time.sleep(10)
