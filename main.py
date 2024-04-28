from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QRubberBand
from PyQt5.QtCore import Qt, pyqtSignal, QRect, QPoint, QSize, QThread
from PyQt5.QtGui import QPixmap, QImage
from PIL import ImageGrab, Image
from io import BytesIO
import ctypes
import sys
from TrueReadClient import TrueReadClient

# Set DPI Awareness
ctypes.windll.shcore.SetProcessDpiAwareness(1)

class Worker(QThread):
    finished = pyqtSignal(bytes)  # Signal to emit audio content

    def __init__(self, image, client):
        super().__init__()
        self.image = image
        self.client = client

    def run(self):
        audio = self.client.get_audio(self.image)
        self.finished.emit(audio)

class AudioPlayer(QThread):
    finished = pyqtSignal()  # Signal to indicate that playback is finished

    def __init__(self, audio_data, client):
        super().__init__()
        self.audio_data = audio_data
        self.client = client

    def run(self):
        self.client.play_audio(self.audio_data)
        self.finished.emit()  # Emit signal when playback finishes

class SnipTool(QWidget):
    screenshot_taken = pyqtSignal(Image.Image)

    def __init__(self, on_close):
        super().__init__()
        self.on_close = on_close
        self.setWindowFlags(Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint)
        self.setWindowOpacity(0.3)
        self.showFullScreen()
        self.rubberBand = QRubberBand(QRubberBand.Rectangle, self)
        self.origin = QPoint()

    def mousePressEvent(self, event):
        self.origin = event.pos()
        self.rubberBand.setGeometry(QRect(self.origin, QSize()))
        self.rubberBand.show()

    def mouseMoveEvent(self, event):
        if not self.origin.isNull():
            self.rubberBand.setGeometry(QRect(self.origin, event.pos()).normalized())

    def mouseReleaseEvent(self, event):
        self.rubberBand.hide()
        if not self.origin.isNull():
            rect = self.rubberBand.geometry()
            screenshot = ImageGrab.grab(bbox=(rect.x(), rect.y(), rect.x() + rect.width(), rect.y() + rect.height()))
            self.screenshot_taken.emit(screenshot)
        self.close()

class MainApplication(QMainWindow):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.trueread_client = TrueReadClient()
        self.audio_content = None  # Store the audio content for playback

    def init_ui(self):
        self.setWindowTitle("TrueRead")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #333333;
            }
            QLabel {
                font-family: 'Arial';
                font-size: 14px;
                color: #FFFFFF;
                text-align: center;
            }
            QPushButton {
                font-family: 'Arial';
                font-size: 14px;
                color: #FFFFFF;
                background-color: #0066CC;
                border: 2px solid #0057D8;
                padding: 10px 20px;  /* Increased padding for better visual and roundness */
                border-radius: 25px;  /* Increased border-radius for more rounded corners */
                min-width: 100px;  /* Ensure enough width to allow for rounded corners */
            }
            QPushButton:hover {
                background-color: #0057D8;
            }
            QPushButton:disabled {
                background-color: #555555;
                border-color: #444444;
                color: #AAAAAA;
            }
        """)

        layout = QVBoxLayout()

        self.button_capture = QPushButton("Take Screenshot")
        self.button_capture.clicked.connect(self.capture_screen)
        layout.addWidget(self.button_capture)

        self.button_upload = QPushButton("Upload Image")
        self.button_upload.clicked.connect(self.upload_image)
        layout.addWidget(self.button_upload)

        self.button_play_audio = QPushButton("Play Audio")
        self.button_play_audio.clicked.connect(self.play_audio)
        self.button_play_audio.setEnabled(False)  # Start with the button disabled
        layout.addWidget(self.button_play_audio)

        self.screenshot_label = QLabel(self)  # Label to display the screenshot
        self.screenshot_label.setFixedSize(600, 400)
        layout.addWidget(self.screenshot_label, alignment=Qt.AlignCenter)  # Center the image

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        self.show()

    def capture_screen(self):
        self.hide()  # Hide the main window
        self.snip_tool = SnipTool(self.display_screenshot)
        self.snip_tool.screenshot_taken.connect(self.display_screenshot)
        self.snip_tool.show()  # Show the snipping tool

    def upload_image(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                   "All Files (*);;Image Files (*.png; *.jpg; *.jpeg)", options=options)
        if file_name:
            image = Image.open(file_name)
            self.display_screenshot(image)

    def display_screenshot(self, screenshot):
        # Save PIL Image to a buffer
        buffer = BytesIO()
        screenshot.save(buffer, format='PNG')
        buffer.seek(0)

        # Create QImage from buffer
        qt_image = QImage()
        qt_image.loadFromData(buffer.read())

        # Convert QImage to QPixmap and display it
        pixmap = QPixmap.fromImage(qt_image)
        self.screenshot_label.setPixmap(pixmap.scaled(self.screenshot_label.size(), Qt.KeepAspectRatio))
        self.show()

        # Start worker thread to get audio content from TrueReadClient
        self.worker = Worker(screenshot, self.trueread_client)
        self.worker.finished.connect(self.handle_audio)
        self.worker.start()

    def handle_audio(self, audio):
        self.audio_content = audio
        if self.audio_content:
            self.button_play_audio.setEnabled(True)  # Enable the button when audio is ready
        else:
            self.button_play_audio.setEnabled(False)  # Disable if no audio content

    def play_audio(self):
        self.button_play_audio.setEnabled(False)  # Disable button during playback
        self.audio_player = AudioPlayer(self.audio_content, self.trueread_client)
        self.audio_player.finished.connect(self.on_audio_finished)  # Connect to slot
        self.audio_player.start()

    def on_audio_finished(self):
        self.button_play_audio.setEnabled(True)  # Re-enable the button after playback

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ex = MainApplication()
    sys.exit(app.exec_())
