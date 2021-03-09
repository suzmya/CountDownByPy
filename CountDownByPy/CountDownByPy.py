import sys
import time
from datetime import datetime, date
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import configparser



def getArgument(secs,key):
    try:
        cf = configparser.ConfigParser()
        cf.read("config.ini")
        #browerArgument = cf.items("BrowserSetting")
        return cf.get(secs,key)
    except Exception as e:
        print (f"检查config.ini文件\nError：{e}")

class MyTimer(QWidget): 
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            #print(f"点击{self.m_Position}::{event.globalPos()}::{self.pos()}")
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #更改鼠标图标
            
    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:  
            self.move(QMouseEvent.globalPos()-self.m_Position)#更改窗口位置
            #print(f"移动{QMouseEvent.globalPos()}::{self.m_Position}")
            QMouseEvent.accept()
            
    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag=False
        self.setCursor(QCursor(Qt.ArrowCursor)) 

    def __init__(self, parent = None):
        super(MyTimer, self).__init__(parent)   
        #self.resize(110, 80)
        self.setGeometry(1200,650, 80, 80)   #窗口 移动到 （300，300） 位置，窗口大小 
        self.setWindowTitle("QTimerDemo")
        self.lb1 = QLabel('111111！',self)

        self.lcd = QLCDNumber(self)   
        self.lcd.setDigitCount(8)#所显示的位数   
        self.lcd.setMode(QLCDNumber.Dec)#十进制
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.display(time.strftime("%X",time.localtime()))
        self.setWindowFlag(Qt.FramelessWindowHint) # 隐藏边框
        self.setWindowOpacity(0.8) # 设置窗口透明度,1.0为不透明状态
        #self.setWindowFlag(Qt.Drawer)#去掉窗口左上角的图标，右上角的最大化最小化按钮
        #self.setAttribute(Qt.WA_TranslucentBackground) # 设置窗口背景透明
        #Qt.SubWindow#隐藏在任务栏的窗口
        #self.lcd.setStyleSheet("border: 2px solid black; color: red; background: silver;")
        
        #垂直布局
        layout = QVBoxLayout()
        layout.addStretch()#添加一个可伸缩空间
        layout.addWidget(self.lb1)
        layout.addWidget(self.lcd)    
        self.setLayout(layout)
     
        #新建一个QTimer对象    
        self.timer = QTimer()   
        self.timer.setInterval(1000)    
        self.timer.start()
      
        # 信号连接到槽    
        self.timer.timeout.connect(self.onTimerOut)
 
    # 定义槽
    def onTimerOut(self):
        #b = datetime.strptime("20:00:00","%X")        
        localTimeStr = time.strftime("%X",time.localtime())
        localTime = datetime.strptime(localTimeStr, "%X")

        if(happyTime<=localTime):
            seconds = (localTime - happyTime).seconds
            self.lb1.setText("加班时长：")
        elif(lunchTime<localTime and localTime<happyTime):
            seconds = (happyTime - localTime).seconds
            self.lb1.setText("距离下班还剩：")
        elif(localTime<=lunchTime):
            seconds = (lunchTime - localTime).seconds
            self.lb1.setText("距离吃饭还剩：")
        
        hour = int(seconds/3600)
        minu = int(seconds/60)-hour*60
        #print(f"{hour}小时{minu}分{seconds%60}秒")
        self.lcd.display(f"{hour}:{minu}:{seconds%60}")
        #self.lcd.display(time.strftime("%X",time.localtime()))
 

        
if __name__ == "__main__": 
    global  happyTime, lunchTime
    happyTimeStr = getArgument("TimeSetting","happyTime")
    lunchTimeStr = getArgument("TimeSetting","lunchTime")
    happyTime = datetime.strptime(happyTimeStr, "%X")
    lunchTime = datetime.strptime(lunchTimeStr, "%X")

    app = QApplication(sys.argv)
    t = MyTimer()
    t.show()
    sys.exit(app.exec_())

