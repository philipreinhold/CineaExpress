from PySide6.QtCore import QRectF

class FrameService:
    def calculate_frame_rect(self, image_rect: QRectF, frame_format: tuple, width_percentage: float) -> QRectF:
        width, height = frame_format
        aspect_ratio = width / height

        frame_width = image_rect.width() * (width_percentage / 100)
        frame_height = frame_width / aspect_ratio

        x = (image_rect.width() - frame_width) / 2
        y = (image_rect.height() - frame_height) / 2

        return QRectF(x, y, frame_width, frame_height)

    def adjust_frame_format(self, current_rect: QRectF, new_format: tuple) -> QRectF:
        width, height = new_format
        aspect_ratio = width / height

        new_height = current_rect.width() / aspect_ratio
        y_offset = (current_rect.height() - new_height) / 2

        return QRectF(current_rect.x(), current_rect.y() + y_offset, current_rect.width(), new_height)

    def adjust_frame_width(self, image_rect: QRectF, current_rect: QRectF, width_percentage: float) -> QRectF:
        new_width = image_rect.width() * (width_percentage / 100)
        scale_factor = new_width / current_rect.width()

        new_height = current_rect.height() * scale_factor
        x_offset = (image_rect.width() - new_width) / 2
        y_offset = (image_rect.height() - new_height) / 2

        return QRectF(x_offset, y_offset, new_width, new_height)

    # Weitere Frame-bezogene Methoden...