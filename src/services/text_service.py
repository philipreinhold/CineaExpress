from PySide6.QtCore import QRectF, QPointF

class TextService:
    def calculate_text_positions(self, frame_rect: QRectF, font_size: int) -> tuple:
        name_pos = frame_rect.topLeft() + QPointF(10, -font_size * 2 - 10)
        desc_pos = frame_rect.topLeft() + QPointF(10, -font_size - 5)
        return name_pos, desc_pos

    def format_scene_text(self, name: str, description: str, max_length: int = 50) -> tuple:
        formatted_name = name[:max_length]
        formatted_desc = description[:max_length] + ('...' if len(description) > max_length else '')
        return formatted_name, formatted_desc

    # Weitere Text-bezogene Methoden...