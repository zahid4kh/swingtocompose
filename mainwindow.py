from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout,
                             QHBoxLayout, QLabel, QPushButton, QTextEdit,
                             QSplitter, QFileDialog, QMessageBox, QProgressBar,
                             QSizePolicy)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QIcon, QColor, QPixmap, QPainter
from streamworker import StreamWorker
from key import GEMINI_API_KEY
from coolstyle import CoolStyle
import sampleswing
from pygmentshighlighter import PygmentsHighlighter, PygmentsFadingEdit
from pygments.lexers import JavaLexer, KotlinLexer


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Swing to Compose Converter (Gemini 2.5)")
        self.setMinimumSize(1200, 800)

        self.init_ui()

    def init_ui(self):
        clear_button_width = 80
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(16, 16, 16, 16)
        main_layout.setSpacing(12)

        title_label = QLabel("Java Swing to Jetpack Compose Converter")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        font = title_label.font()
        font.setPointSize(16)
        font.setBold(True)
        title_label.setFont(font)
        main_layout.addWidget(title_label)

        splitter = QSplitter(Qt.Orientation.Horizontal)

        input_widget = QWidget()
        input_layout = QVBoxLayout(input_widget)
        input_layout.setContentsMargins(0, 0, 0, 0)

        input_header_layout = QHBoxLayout()
        input_label = QLabel("Java Swing Code")
        input_clear_button = QPushButton("Clear")
        # input_clear_button.setFixedWidth(clear_button_width)
        input_header_layout.addWidget(input_label)
        input_header_layout.addStretch()
        input_header_layout.addWidget(input_clear_button)
        input_layout.addLayout(input_header_layout)

        self.swing_editor = QTextEdit()
        self.swing_editor.setFont(CoolStyle.get_code_font())
        self.swing_editor.setPlaceholderText(
            "Paste your Java Swing code here...")
        self.swing_editor.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.java_highlighter = PygmentsHighlighter(
            self.swing_editor.document(), JavaLexer())
        input_layout.addWidget(self.swing_editor)

        output_widget = QWidget()
        output_layout = QVBoxLayout(output_widget)
        output_layout.setContentsMargins(0, 0, 0, 0)

        output_header_layout = QHBoxLayout()
        output_label = QLabel("Jetpack Compose Code")
        output_clear_button = QPushButton("Clear")
        # output_clear_button.setFixedWidth(clear_button_width)
        output_header_layout.addWidget(output_label)
        output_header_layout.addStretch()
        output_header_layout.addWidget(output_clear_button)
        output_layout.addLayout(output_header_layout)

        self.compose_output = PygmentsFadingEdit(lexer=KotlinLexer())
        self.compose_output.setFont(CoolStyle.get_code_font())
        self.compose_output.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        output_layout.addWidget(self.compose_output)

        input_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        output_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        splitter.addWidget(input_widget)
        splitter.addWidget(output_widget)
        splitter.setSizes([600, 600])

        splitter.setSizePolicy(QSizePolicy.Policy.Expanding,
                               QSizePolicy.Policy.Expanding)
        main_layout.addWidget(splitter)

        self.progress_bar = QProgressBar()
        self.progress_bar.setTextVisible(False)
        self.progress_bar.setRange(0, 0)
        self.progress_bar.hide()
        main_layout.addWidget(self.progress_bar)

        button_layout = QHBoxLayout()

        icon_path = "icons/"
        reload_icon = self.create_white_icon(icon_path + "reload.svg")
        save_icon = self.create_white_icon(icon_path + "save.svg")
        load_sample_icon = self.create_white_icon(
            icon_path + "load_document.svg")
        java_icon = self.create_white_icon(icon_path + "java.svg")

        self.load_button = QPushButton(java_icon, "Load From File")
        self.convert_button = QPushButton(reload_icon, "Convert with Gemini")
        self.save_button = QPushButton(save_icon, "Save Output")
        self.load_sample_button = QPushButton(load_sample_icon, "Load Sample")

        outlined_style = """
            QPushButton {
                background-color: transparent;
                color: #CCCCCC;
                border: 1px solid #666666;
                padding: 8px 16px;
                border-radius: 7px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: rgba(255, 255, 255, 0.1);
                border: 1px solid #888888;
            }

            QPushButton:pressed {
                background-color: rgba(255, 255, 255, 0.2);
                border: 1px solid #AAAAAA;
            }
        """
        self.load_button.setStyleSheet(outlined_style)
        self.convert_button.setStyleSheet(outlined_style)
        self.save_button.setStyleSheet(outlined_style)
        self.load_sample_button.setStyleSheet(outlined_style)
        input_clear_button.setStyleSheet(outlined_style)
        output_clear_button.setStyleSheet(outlined_style)

        self.convert_button.setMinimumWidth(200)
        font = self.convert_button.font()
        font.setBold(True)
        self.convert_button.setFont(font)

        self.load_button.clicked.connect(self.load_file)
        self.convert_button.clicked.connect(self.convert_code)
        self.save_button.clicked.connect(self.save_file)
        self.load_sample_button.clicked.connect(self.load_sample)
        input_clear_button.clicked.connect(self.clear_input)
        output_clear_button.clicked.connect(self.clear_output)

        button_layout.addWidget(self.load_button)
        button_layout.addWidget(self.load_sample_button)
        button_layout.addStretch()
        button_layout.addWidget(self.convert_button)
        button_layout.addStretch()
        button_layout.addWidget(self.save_button)

        main_layout.addLayout(button_layout)

        api_status_layout = QHBoxLayout()
        if not GEMINI_API_KEY:
            api_status = QLabel(
                "⚠️ No Gemini API key found - running in demo mode")
            api_status.setStyleSheet("color: #FFA500;")
        else:
            api_status = QLabel("✓ Gemini API connected")
            api_status.setStyleSheet("color: #00FF00;")
        api_status_layout.addWidget(api_status)
        api_status_layout.addStretch()
        main_layout.addLayout(api_status_layout)

        self.setCentralWidget(central_widget)

    def create_white_icon(self, icon_path):
        pixmap = QPixmap(icon_path)

        white_pixmap = QPixmap(pixmap.size())
        white_pixmap.fill(QColor(0, 0, 0, 0))

        painter = QPainter(white_pixmap)
        painter.setCompositionMode(
            QPainter.CompositionMode.CompositionMode_Source)
        painter.drawPixmap(0, 0, pixmap)
        painter.setCompositionMode(
            QPainter.CompositionMode.CompositionMode_SourceIn)
        painter.fillRect(white_pixmap.rect(), QColor(255, 255, 255))
        painter.end()

        return QIcon(white_pixmap)

    def convert_code(self):
        swing_code = self.swing_editor.toPlainText()

        if not swing_code.strip():
            QMessageBox.warning(
                self, "Warning", "Please enter some Java Swing code first.")
            return

        self.compose_output.clear()

        self.progress_bar.show()
        self.set_buttons_enabled(False)

        self.worker = StreamWorker(swing_code)

        self.worker.chunk_received.connect(self.on_chunk_received)
        self.worker.finished.connect(self.on_conversion_finished)
        self.worker.error.connect(self.on_conversion_error)

        self.worker.start()

    def on_chunk_received(self, chunk):
        self.compose_output.append_with_fade(chunk)

    def on_conversion_finished(self):
        self.progress_bar.hide()
        self.set_buttons_enabled(True)

    def on_conversion_error(self, error_msg):
        self.progress_bar.hide()
        self.set_buttons_enabled(True)
        QMessageBox.critical(
            self, "Error", f"Error during conversion: {error_msg}")

    def set_buttons_enabled(self, enabled):
        self.convert_button.setEnabled(enabled)
        self.load_button.setEnabled(enabled)
        self.save_button.setEnabled(enabled)
        self.load_sample_button.setEnabled(enabled)

    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Open Java File",
            "",
            "Java Files (*.java);;All Files (*)"
        )

        if file_name:
            try:
                with open(file_name, 'r') as file:
                    self.swing_editor.setPlainText(file.read())
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Could not open file: {str(e)}")

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Compose File",
            "",
            "Kotlin Files (*.kt);;All Files (*)"
        )

        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(self.compose_output.toPlainText())
            except Exception as e:
                QMessageBox.critical(
                    self, "Error", f"Could not save file: {str(e)}")

    def load_sample(self):
        sample_code = sampleswing.sample_code
        self.swing_editor.setPlainText(sample_code)

    def clear_input(self):
        self.swing_editor.clear()

    def clear_output(self):
        self.compose_output.clear()
