from PySide2.QtGui import *
from PySide2.QtWidgets import *
from PySide2.QtCore import *
import cv2
import numpy as np
import sys
from ui_gui import Ui_MainWindow
from PyQt5.QtCore import pyqtSignal, QThread
from tkinter.filedialog import askopenfilename
import base64
import requests

VIDEO_PATH = 0
url = 'http://127.0.0.1:5000/process_image'
RUN_PROCESSING = True

# thread to run for camera
class CameraThread(QThread):
    update_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)

    def process_frame(self,frame):
        global url
        _, img_encoded = cv2.imencode('.jpg', frame)
        img_bytes = img_encoded.tobytes()
        files = {'image': img_bytes}
        response = requests.post(url, files=files)
        if response.status_code == 200:
            result = response.json()
            image_base64 = result.get('image_base64')
            status = result.get('status')

        # Decode base64 image
        img_data = base64.b64decode(image_base64)
        nparr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if len(status) == 0:
            status = 'None'
        else:
            status = status[0]

        cv2.putText(img,str(status),(30,30),cv2.FONT_HERSHEY_COMPLEX,1,(0,255,0),1)
        
        return img

    def run(self):
        global VIDEO_PATH, RUN_PROCESSING
        cap = cv2.VideoCapture(VIDEO_PATH)
        while True:
            ret, frame = cap.read()
            if not ret:
                print("VIDEO ENDED")
                self.update_signal.emit(np.zeros((500, 500, 3), dtype=np.uint8))

            if RUN_PROCESSING:
                frame = self.process_frame(frame)
            else:
                self.msleep(30)

            self.update_signal.emit([frame])


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.start_btn.clicked.connect(lambda: self.start_processing())
        self.ui.select_video_btn.clicked.connect(lambda: self.pick_file())
        self.camera_thread4 = CameraThread()
        self.camera_thread4.update_signal.connect(self.main_loop)

    def pick_file(self):
        file = askopenfilename()
        if file != '':
            self.ui.source_txt.setText(file)

    def start_processing(self):
        global VIDEO_PATH, RUN_PROCESSING
        if self.ui.start_btn.text() == 'Start':
            RUN_PROCESSING = True
            self.ui.start_btn.setText('Stop')
            
            video_path = self.ui.source_txt.text()
            if video_path == '':
                return
            
            if video_path.isnumeric():
                video_path = int(video_path)
            
            VIDEO_PATH = video_path
            
            # Define the codec and create a VideoWriter object
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            cap = cv2.VideoCapture(VIDEO_PATH)
            ret, frame = cap.read()
            h,w,_ = frame.shape
            self.out = cv2.VideoWriter('output.avi', fourcc, 20.0, (w, h))
            cap.release()
            
            self.camera_thread4.start()
        else:
            RUN_PROCESSING = False
            self.out.release()
            self.ui.start_btn.setText('Start')

    def main_loop(self, pixmaps):
        try:
            frame = pixmaps[0]
        except:
        
            return
        
        self.out.write(frame)
        self.set_camera_frame(frame, self.ui.camera_lbl)

    def set_camera_frame(self, frame, label):
        """
        This function sets frame to view
        it takes a frame and a label and sets that frame as labels background
        """
        
        frame = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(qImg)

        label.setPixmap(pixmap)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
