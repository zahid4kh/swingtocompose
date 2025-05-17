import time
from PyQt6.QtCore import pyqtSignal, QThread
import google.generativeai as genai
from key import GEMINI_API_KEY
from prompts import SWING_TO_COMPOSE_PROMPT
import samplecompose


class StreamWorker(QThread):
    chunk_received = pyqtSignal(str)
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, swing_code: str):
        super().__init__()
        self.swing_code = swing_code

    def run(self):
        try:
            if not GEMINI_API_KEY:
                self._simulate_response()
                return

            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash-preview-04-17",
                generation_config={
                    "temperature": 0.2,
                    "top_p": 0.8,
                    "top_k": 40
                }
            )

            prompt = SWING_TO_COMPOSE_PROMPT.format(swing_code=self.swing_code)

            response = model.generate_content(prompt, stream=True)

            for chunk in response:
                if chunk.text is not None:
                    self.chunk_received.emit(chunk.text)
                    time.sleep(0.05)
                elif hasattr(chunk, 'parts') and chunk.parts:
                    for part in chunk.parts:
                        if part.text:
                            self.chunk_received.emit(part.text)
                            time.sleep(0.05)

            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))

    def _simulate_response(self):

        sample_code = samplecompose.sample_code
        # only simulating streaming here
        chunks = [sample_code[i:i+20] for i in range(0, len(sample_code), 20)]

        for chunk in chunks:
            self.chunk_received.emit(chunk)
            time.sleep(0.05)

        self.finished.emit()
