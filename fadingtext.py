
import time
from PyQt6.QtWidgets import (QApplication, QTextEdit)
from PyQt6.QtGui import QColor, QTextCharFormat, QTextCursor


class FadingTextEdit(QTextEdit):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.chunks_to_animate = []
        self.currently_animating = False

    def append_with_fade(self, text: str):
        self.chunks_to_animate.append(text)
        if not self.currently_animating:
            self._animate_next_chunk()

    def _animate_next_chunk(self):
        if not self.chunks_to_animate:
            self.currently_animating = False
            return

        self.currently_animating = True
        chunk = self.chunks_to_animate.pop(0)

        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)

        initial_format = QTextCharFormat()
        initial_format.setForeground(QColor(0, 0, 0, 0))  # Fully transparent
        cursor.insertText(chunk, initial_format)

        # animation
        self._animate_last_chunk(len(chunk))

    def _animate_last_chunk(self, chunk_length: int):
        """Apply fade-in animation to the last added chunk"""
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.movePosition(QTextCursor.MoveOperation.Left,
                            QTextCursor.MoveMode.KeepAnchor, chunk_length)

        # sequence
        for alpha in range(0, 256, 15):
            format = QTextCharFormat()
            format.setForeground(QColor(0, 0, 0, alpha))
            cursor.setCharFormat(format)
            QApplication.processEvents()
            time.sleep(0.01)

        format = QTextCharFormat()
        format.setForeground(QColor(0, 0, 0, 255))
        cursor.setCharFormat(format)

        QApplication.processEvents()
        self._animate_next_chunk()
