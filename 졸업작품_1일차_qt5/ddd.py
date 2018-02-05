#1일차
#qtcreator로 ui 만들고 python에서 받아오고 받아온 객체의 기능을 구현한다.
import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

form_class = uic.loadUiType("main_window.ui")[0]


##class 지정 form 은 designer로 만든 ui로 지정.
##첫번째 인자 QmainWindow는 메인 window 라는 뜻.
class MyWindow(QMainWindow,form_class):

 ##초기화 부분 ui 설정함. 그리고 푸쉬버튼 객체를 slot1 이라는 핸들러에게 전달시켜줌.
 def __init__(self):
  super().__init__()
  self.setupUi(self)
  self.pushButton.clicked.connect(self.slot1)


##푸쉬버튼 이벤트 발생시 동작하는 핸들러. 라벨을 바꾼다.
 def slot1(self):
   self.label.setText("click")




##이 창이 main 창일때(즉 다른 곳에서 모듈로 끌어올 때는 이창이 메인이 아니므로 실행이 되지 않음)
##객체화해서 보여주는 것 같음. 아직 모르는 부분 31열~. ,
if __name__=="__main__":
 app=QApplication(sys.argv)
 myWindow=MyWindow()
 myWindow.show()
 app.exec_()



