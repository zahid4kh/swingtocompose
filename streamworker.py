import time
from PyQt6.QtCore import pyqtSignal, QThread
import google.generativeai as genai
from key import GEMINI_API_KEY
from samplecompose import sample_code


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
                model_name="gemini-2.5-flash",
                generation_config={
                    "temperature": 0.2,
                    "top_p": 0.95,
                    "top_k": 32,
                }
            )

            prompt = f"""
            You are a professional code converter specializing in transforming Java Swing code to Jetpack Compose for Desktop.
            
            Please convert the following Java Swing code to equivalent Jetpack Compose for Desktop code (Kotlin):
            
            ```java
            {self.swing_code}
            ```
            
            Your conversion should:
            1. Preserve all functionality of the original Swing application
            2. Use modern Compose for Desktop practices and patterns
            3. Handle layouts appropriately (converting layout managers to Compose layout concepts)
            4. Convert action listeners to Compose event handling
            5. Use Compose state management instead of imperative variable changes
            6. Add necessary imports
            
            Respond ONLY with the complete Kotlin code that uses Compose for Desktop, with no additional explanation or comments outside the code.
            """

            response = model.generate_content(prompt, stream=True)

            for chunk in response:
                if hasattr(chunk, 'text') and chunk.text:
                    self.chunk_received.emit(chunk.text)
                    time.sleep(0.05)

            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))

    def _simulate_response(self):

        sample_code = sample_code
        # only simulating streaming here
        chunks = [sample_code[i:i+20] for i in range(0, len(sample_code), 20)]

        for chunk in chunks:
            self.chunk_received.emit(chunk)
            time.sleep(0.05)

        self.finished.emit()
