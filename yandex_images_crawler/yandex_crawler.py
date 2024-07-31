import logging
import time
from multiprocessing import Queue, Value, get_logger

from selenium import webdriver
from selenium.webdriver.common.by import By


class YandexCrawler:
    def __init__(
        self,
        start_link: str,
        load_queue: Queue,
        id=0,
        is_active=Value("i", True),
    ):
        self.start_link: str = start_link
        self.load_queue: Queue = load_queue
        self.id: str = str(id)
        self.is_active = is_active

        self.driver = webdriver.Firefox()

        self.logger: logging.Logger = get_logger()
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter("%(levelname)s - %(asctime)s - %(message)s"))
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def __get_image_link(self):
        width, height = None, None

        size_sources = [
            "OpenImageButton-SizesButton",
            "MMViewerButtons-ImageSizes",
            "OpenImageButton-SaveSize",
            "Button2-Text",
        ]

        for source in size_sources:
            if width is not None and height is not None:
                break
            for elem in self.driver.find_elements(By.CLASS_NAME, source):
                try:
                    width, height = [int(i) for i in elem.text.split("×")]
                    break
                except:
                    pass
        else:
            if width is None or height is None:
                self.logger.critical(f"Process #{self.id} can't get image size.")
                return

        link = None

        link_sources = [
            "OpenImageButton-Save",
            "MMViewerButtons-OpenImage",
            "MMViewerButtons-Button",
            "Button2_link",
            "Button2_view_default",
        ]

        blacklist = [
            "yandex-images",
            "avatars.mds.yandex.net",
        ]

        for source in link_sources:
            if link is not None:
                break
            for elem in self.driver.find_elements(By.CLASS_NAME, source):
                try:
                    link = elem.get_attribute("href")
                    for b in blacklist:
                        if b in link:
                            time.sleep(5)
                            link = elem.get_attribute("href")
                            break
                    break
                except:
                    pass
        else:
            if link is None:
                self.logger.critical(f"Process #{self.id} can't get image link.")
                return

        self.load_queue.put((link, (width, height)))

    def __next_preview(self):
        try:
            btn = self.driver.find_element(By.CSS_SELECTOR, "button[class*='CircleButton_type_next']")
            btn.click()
        except:
            self.logger.critical(f"Process #{self.id} can't move to the next image.")

    def run(self):
        self.driver.get(self.start_link)
        while True:
            if not self.is_active.value:
                self.driver.close()
                return

            try:
                self.__get_image_link()
                self.__next_preview()
            except Exception as e:
                self.logger.critical(e)
                time.sleep(10)
