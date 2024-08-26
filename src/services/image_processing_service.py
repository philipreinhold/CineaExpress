import logging
from PySide6.QtGui import QImage
from PIL import Image, ImageEnhance, ImageOps
import numpy as np

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class ImageProcessingService:
    def load_image(self, image_path: str) -> QImage:
        try:
            image = QImage(image_path)
            if image.isNull():
                raise ValueError(f"Failed to load image from {image_path}")
            logger.info(f"Image loaded from {image_path}")
            return image
        except Exception as e:
            logger.error(f"Error loading image: {str(e)}")
            raise

    def save_image(self, image: QImage, file_path: str):
        try:
            if not image.save(file_path):
                raise ValueError(f"Failed to save image to {file_path}")
            logger.info(f"Image saved to {file_path}")
        except Exception as e:
            logger.error(f"Error saving image: {str(e)}")
            raise

    def qimage_to_pil(self, qimage: QImage) -> Image.Image:
        try:
            """Convert QImage to PIL Image."""
            # Get the dimensions of the QImage
            width = qimage.width()
            height = qimage.height()

            # Get the format of the QImage
            format = qimage.format()

            # Convert QImage to bytes
            bits = qimage.bits()
            bits.setsize(height * width * 4)  # 4 bytes per pixel (RGBA)
            arr = np.frombuffer(bits, np.uint8).reshape((height, width, 4))

            # Convert to correct color format
            if format == QImage.Format_RGB32:
                arr = arr[:,:,:3]
            elif format == QImage.Format_ARGB32:
                arr = arr[:,:,[2,1,0,3]]  # BGRA to RGBA

            # Create PIL Image
            if arr.shape[2] == 3:
                image = Image.fromarray(arr, 'RGB')
            elif arr.shape[2] == 4:
                image = Image.fromarray(arr, 'RGBA')
            else:
                raise ValueError(f"Unexpected number of channels: {arr.shape[2]}")

            return image

        except Exception as e:
            logger.error(f"Error converting QImage to PIL: {str(e)}")
            raise
    
    def pil_to_qimage(self, pil_image: Image.Image) -> QImage:
        try:
            if pil_image.mode == "RGB":
                r, g, b = pil_image.split()
                pil_image = Image.merge("RGB", (b, g, r))
            elif pil_image.mode == "RGBA":
                r, g, b, a = pil_image.split()
                pil_image = Image.merge("RGBA", (b, g, r, a))
            
            im2 = pil_image.convert("RGBA")
            data = im2.tobytes("raw", "RGBA")
            qimage = QImage(data, im2.size[0], im2.size[1], QImage.Format_RGBA8888)
            logger.debug("PIL Image converted to QImage")
            return qimage
        except Exception as e:
            logger.error(f"Error converting PIL to QImage: {str(e)}")
            raise

    def adjust_brightness(self, image: QImage, value: float) -> QImage:
        try:
            pil_image = self.qimage_to_pil(image)
            enhancer = ImageEnhance.Brightness(pil_image)
            adjusted = enhancer.enhance(1 + value / 100)
            logger.debug(f"Brightness adjusted by {value}")
            return self.pil_to_qimage(adjusted)
        except Exception as e:
            logger.error(f"Error adjusting brightness: {str(e)}")
            raise

    def adjust_contrast(self, image: QImage, value: float) -> QImage:
        try:
            pil_image = self.qimage_to_pil(image)
            enhancer = ImageEnhance.Contrast(pil_image)
            adjusted = enhancer.enhance(1 + value / 100)
            logger.debug(f"Contrast adjusted by {value}")
            return self.pil_to_qimage(adjusted)
        except Exception as e:
            logger.error(f"Error adjusting contrast: {str(e)}")
            raise

    def apply_grayscale(self, image: QImage, intensity: float) -> QImage:
        try:
            pil_image = self.qimage_to_pil(image)
            gray_image = ImageOps.grayscale(pil_image)
            blended = Image.blend(pil_image.convert("RGB"), gray_image.convert("RGB"), intensity / 100)
            logger.debug(f"Grayscale applied with intensity {intensity}")
            return self.pil_to_qimage(blended)
        except Exception as e:
            logger.error(f"Error applying grayscale: {str(e)}")
            raise

    def sepia_filter(self, image: Image.Image) -> Image.Image:
        try:
            img_array = np.array(image)
            sepia_filter = np.array([
                [0.393, 0.769, 0.189],
                [0.349, 0.686, 0.168],
                [0.272, 0.534, 0.131]
            ])
            sepia_img = np.clip(img_array.dot(sepia_filter.T), 0, 255).astype(np.uint8)
            return Image.fromarray(sepia_img)
        except Exception as e:
            logger.error(f"Error applying sepia filter: {str(e)}")
            raise

    def apply_sepia(self, image: QImage, intensity: float) -> QImage:
        try:
            pil_image = self.qimage_to_pil(image)
            sepia_image = self.sepia_filter(pil_image)
            blended = Image.blend(pil_image.convert("RGB"), sepia_image, intensity / 100)
            logger.debug(f"Sepia applied with intensity {intensity}")
            return self.pil_to_qimage(blended)
        except Exception as e:
            logger.error(f"Error applying sepia: {str(e)}")
            raise

    def rotate_image(self, image: QImage) -> QImage:
        try:
            pil_image = self.qimage_to_pil(image)
            rotated = pil_image.rotate(90, expand=True)
            logger.debug("Image rotated 90 degrees")
            return self.pil_to_qimage(rotated)
        except Exception as e:
            logger.error(f"Error rotating image: {str(e)}")
            raise

    def flip_image_horizontal(self, image: QImage) -> QImage:
        try:
            pil_image = self.qimage_to_pil(image)
            flipped = pil_image.transpose(Image.FLIP_LEFT_RIGHT)
            logger.debug("Image flipped horizontally")
            return self.pil_to_qimage(flipped)
        except Exception as e:
            logger.error(f"Error flipping image horizontally: {str(e)}")
            raise

    def flip_image_vertical(self, image: QImage) -> QImage:
        try:
            pil_image = self.qimage_to_pil(image)
            flipped = pil_image.transpose(Image.FLIP_TOP_BOTTOM)
            logger.debug("Image flipped vertically")
            return self.pil_to_qimage(flipped)
        except Exception as e:
            logger.error(f"Error flipping image vertically: {str(e)}")
            raise