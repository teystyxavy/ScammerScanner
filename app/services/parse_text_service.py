from PIL import Image
from config import Config
import pytesseract
import cv2

class ParseTextService:
    def __init__(self) -> None:
        pytesseract.pytesseract.tesseract_cmd = Config.TESSERACT_PATH
        pass

    def load_image(self, image_path:str) -> Image:
        """
        Load image and greyscale
        Returns PIL image
        """
        image = cv2.imread(image_path,0)
        PIL_image = Image.fromarray(image)
        return PIL_image

    def extract_text(self, image:Image.Image) -> str:
        """
        Extract all text from image
        """
        return pytesseract.image_to_string(image, lang='eng', config='--psm 6')

