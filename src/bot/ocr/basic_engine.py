import io

import cv2
import numpy as np
import pytesseract
from PIL import Image

from logger import get_default_logger
from parameters import parameters
from utils import format_text

pytesseract.pytesseract.tesseract_cmd = parameters["tesseract_path"]
ocr_logger = get_default_logger("ocr")


def process_image(image_array: np.ndarray) -> np.ndarray:
    image_array = cv2.cvtColor(image_array, cv2.COLOR_BGR2GRAY)
    return image_array


def scan_text(image_bytes: bytes) -> (str, str):
    try:
        image_array: np.ndarray = np.array(Image.open(io.BytesIO(image_bytes)))
        prepared_image_array: np.ndarray = process_image(image_array)
        raw_text_lat = pytesseract.image_to_string(prepared_image_array, lang="eng")
        raw_text_cyr = pytesseract.image_to_string(prepared_image_array, lang="rus")
        return format_text(raw_text_lat), format_text(raw_text_cyr)
    except Exception as ex:
        ocr_logger.info(f"failed ocr: {ex}")
