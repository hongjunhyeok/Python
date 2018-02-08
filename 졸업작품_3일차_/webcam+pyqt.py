from PyQt4 import QtCore, QtGui, uic
import sys
import cv2
import numpy as np
import threading
import time
import queue

running = False
capture_thread = None
form_class = uic.loadUiType("simple.ui")[0]
q=queue.Queue()

##비디오 캡쳐 설정해주는 부분
##cam = 0 or 1
##running = while control
def grab(cam, queue, width, height, fps):
    global running
    capture = cv2.VideoCapture(cam)
    capture.set(cv2.CAP_PROP_FRAME_WIDTH, width)
    capture.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
    capture.set(cv2.CAP_PROP_FPS, fps)

#frame의 'img'key는 img value를 갖는다.
#queue는 저장역할을 맡는다.
    while (running):
        frame = {}
        capture.grab()
        retval, img = capture.read(0)
        frame["img"] = img
        ##컴퓨터 구조와 관련있는 코드인데 q의 크기가 크면 보내는데 지연이 많이 생기는 것으로 이해하고 있다.
        ##좀더 파악할 필요성이 있다.
        if queue.qsize() < 10:
            queue.put(frame)
        else:
            print(queue.qsize())


class OwnImageWidget(QtGui.QWidget):
    def __init__(self, parent=None):
        super(OwnImageWidget, self).__init__(parent)
        self.image = None

    def setImage(self, image):
        self.image = image
        sz = image.size()
        self.setMinimumSize(sz)
        self.update()

    def paintEvent(self, event):
        qp = QtGui.QPainter()
        qp.begin(self)
        if self.image:
            qp.drawImage(QtCore.QPoint(0, 0), self.image)
        qp.end()


class MyWindowClass(QtGui.QMainWindow, form_class):
    def __init__(self, parent=None):
        QtGui.QMainWindow.__init__(self, parent)
        self.setupUi(self)

        self.startButton.clicked.connect(self.start_clicked)

        self.window_width = self.ImgWidget.frameSize().width()
        self.window_height = self.ImgWidget.frameSize().height()
        self.ImgWidget = OwnImageWidget(self.ImgWidget)

        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(1)



##시작 버튼을 누를때 thread 실행.
    def start_clicked(self):
        global running
        running = True
        capture_thread.start()
        self.startButton.setEnabled(False)  ##버튼 비활성화.
        self.startButton.setText('Starting...')


##frame을 업데이트시킴
## q가 비지 않는 경우에만 >>> queue에 보낼게 있는경우에만 >>>queue엔 frame이 들어있음.
    def update_frame(self):
        if not q.empty():
            self.startButton.setText('Camera is live')
            frame = q.get() ## frame을 지속적으로 set 시켜줌.
            img = frame["img"]

            ##3일차 numpy부분 참고. shape는 행렬로 되어있음. 각각의 행이 height width color로 들어감.
            img_height, img_width, img_colors = img.shape
            scale_w = float(self.window_width) / float(img_width)
            scale_h = float(self.window_height) / float(img_height)
            scale = min([scale_w, scale_h])

            if scale == 0:
                scale = 1

            img = cv2.resize(img, None, fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            height, width, bpc = img.shape
            bpl = bpc * width
            image = QtGui.QImage(img.data, width, height, bpl, QtGui.QImage.Format_RGB888)
            self.ImgWidget.setImage(image)

    def closeEvent(self, event):
        global running
        running = False


capture_thread = threading.Thread(target=grab, args=(0, q, 1920, 1080, 30))

app = QtGui.QApplication(sys.argv)
w = MyWindowClass(None)
w.setWindowTitle(' PyQT OpenCV USB camera test panel')
w.show()
app.exec_()