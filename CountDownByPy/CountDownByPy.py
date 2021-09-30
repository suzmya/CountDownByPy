import sys
import time
from datetime import datetime, date
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
import configparser
import os
from datetime import datetime

#testtesttest2
def cctest(str)
     #print ("cctest！！！！！！！！！！！！！！！！？？？")
def getArgument(secs,key):
    try:
        cf = configparser.ConfigParser()
        cf.read("config.ini")
        #browerArgument = cf.items("BrowserSetting")
        return cf.get(secs,key)
    except Exception as e:
        #print (f"检查config.ini文件\nError：{e}")
        writeErrLog(e)
        

def writeErrLog(str):
    curPath = os.path.abspath(os.path.dirname(__file__))#E:\VS\GIT\CountDownByPy\CountDownByPy
    now = datetime.now()
    fileName = now.strftime("%Y-%m-%d")
    textStr = now.strftime("%H:%M:%S")
    with open(f"{curPath}\\{fileName}.txt","a",encoding='utf-8') as f:
        f.write(f"{textStr}:{str}\n")
        pass

class MyTimer(QWidget): 
    def mousePressEvent(self, event):
        if event.button()==Qt.LeftButton:
            self.m_flag=True
            self.m_Position=event.globalPos()-self.pos() #获取鼠标相对窗口的位置
            #print(f"点击{self.m_Position}::{event.globalPos()}::{self.pos()}")
            event.accept()
            self.setCursor(QCursor(Qt.OpenHandCursor))  #更改鼠标图标
        if event.button()==Qt.RightButton:
            #self.close()
            menu = QMenu(self)
            quitAction = menu.addAction("Quit")
            action = menu.exec_(self.mapToGlobal(event.pos()))
            if action == quitAction:
                qApp.quit()

            
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
        #try:
        #    self.setGeometry(1200,650, 80, 70)
        #    pass
        #except Exception as e:
        #    print(e)
        self.setGeometry(1200,650, 80, 70)   #窗口 移动到 （1200，650） 位置，窗口大小 
        self.setWindowTitle("CountDown")
        
        
        self.lbStr = lbStrTemp
        self.lb1 = QLabel()
        """ 计算文本的总宽度 """
        fontMetrics = QFontMetrics(QFont('Microsoft YaHei', 10, 50))
        self.nameWidth = sum([fontMetrics.width(i)
                                    for i in self.lbStr])
        #print(self.nameWidth)
        """ 根据字符串长度调整窗口宽度 """
        # 判断是否有字符串宽度超过窗口的最大宽度
        self.isNameTooLong = self.nameWidth > 70
        # 设置窗口的宽度
        self.setFixedWidth(min(self.nameWidth, 100))

        # 设置刷新时间和移动距离
        self.timeStepLcd = 1000
        self.timeStepLb = 100
        self.moveStep = 1
        self.lbCurrentIndex = 0
        # 设置字符串溢出标志位
        self.isAllOut = False
        # 设置两段字符串之间留白的宽度
        self.spacing = 10

        self.lcd = QLCDNumber(self)   
        self.lcd.setMaximumWidth(70)#设置LCD最大宽度
        self.lcd.setDigitCount(8)#所显示的位数   
        self.lcd.setMode(QLCDNumber.Dec)#十进制
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.display(time.strftime("%X",time.localtime()))
        self.setWindowFlag(Qt.FramelessWindowHint) # 隐藏边框
        self.setWindowOpacity(0.8) # 设置窗口透明度,1.0为不透明状态
        #self.setWindowFlag(Qt.Drawer)#去掉窗口左上角的图标，右上角的最大化最小化按钮
        self.setAttribute(Qt.WA_TranslucentBackground) # 设置窗口背景透明
        self.setWindowFlag(Qt.SubWindow)#隐藏在任务栏的窗口

        self.lcd.setStyleSheet(lcdStyle)#设置LCD格式
        
        #垂直布局
        layout = QVBoxLayout()
        layout.addStretch()#添加一个可伸缩空间
        layout.addWidget(self.lb1)
        layout.addWidget(self.lcd)    
        self.setLayout(layout)
        
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint);
        self.showNormal();#将窗口恢复到初始大小
        
        #新建一个QTimerLCD对象    
        self.timerLcd = QTimer()   
        self.timerLcd.setInterval(self.timeStepLcd)    
        self.timerLcd.start()     
        # 信号连接到槽    
        self.timerLcd.timeout.connect(self.onTimerOutLcd)
 
        #新建一个QTimerLb对象    
        self.timerLb = QTimer()   
        self.timerLb.setInterval(self.timeStepLb)    
        self.timerLb.start()      
        # 信号连接到槽    
        self.timerLb.timeout.connect(self.onTimerOutLb)


    # 定义槽Lcd
    def onTimerOutLcd(self):
        
        #b = datetime.strptime("20:00:00","%X")        
        localTimeStr = time.strftime("%X",time.localtime())
        localTime = datetime.strptime(localTimeStr, "%X")
        #localTime = time.localtime()#(2021, 3, 11, 22, 27, 40, 3, 70, 0)

        if(happyTime<=localTime):
            seconds = (localTime - happyTime).seconds
            #self.lb1.setText("加班时长：")
            if seconds>3600:
                self.lbStr =  lbHappyStr
        elif(lunchTime<localTime and localTime<happyTime):
            seconds = (happyTime - localTime).seconds
            self.lbStr =  lbStrTemp
            if (localTime - lunchTime).seconds < timeSpanInt:
                self.lbStr = lbLunchStr
            #self.lb1.setText("距离下班还剩：")
        elif(localTime<=lunchTime):
            seconds = (lunchTime - localTime).seconds
            #self.lb1.setText("距离吃饭还剩：")
            self.lbStr =  lbStrTemp
        
        hour = int(seconds/3600)
        hour = hour if hour>=10 else "0"+ str(hour)

        minu = int(seconds/60)-int(hour)*60
        minu = minu if minu>=10 else "0"+str(minu)
        
        ss = seconds%60
        ss = ss if ss>=10 else "0"+str(ss)

        #print(f"{hour}小时{minu}分{seconds%60}秒")
        self.lcd.display(f"{hour}:{minu}:{ss}")
        #print("onTimerOutLcd")
        #self.lcd.display(time.strftime("%X",time.localtime()))

    # 定义槽Lb
    def onTimerOutLb(self):
        
        global lbStr
        self.update()
        #lbStr = lbStr[1:]+lbStr[0]
        #self.lb1.setText(lbStr)
        self.lbCurrentIndex += 1
        # 设置下标重置条件
        resetIndexCond = self.lbCurrentIndex * \
            self.moveStep >= self.nameWidth + self.spacing * self.isAllOut
        # 只要条件满足就要重置下标并将字符串溢出置位，保证在字符串溢出后不会因为留出的空白而发生跳变
        if resetIndexCond:
            self.lbCurrentIndex = 0
            self.isAllOut = True
        #print("LbLbLbLb")

    def paintEvent(self, e):
        """ 绘制文本 """
        # super().paintEvent(e)       
        painter = QPainter(self)
        painter.setPen(Qt.black)
        # 绘制字符串
        painter.setFont(QFont('Microsoft YaHei', 10))
        if self.isNameTooLong:
            # 实际上绘制了两段完整的字符串
            # 从负的横坐标开始绘制第一段字符串
            painter.drawText(self.spacing * self.isAllOut - self.moveStep *
                             self.lbCurrentIndex, 35, self.lbStr)
            # 绘制第二段字符串
            painter.drawText(self.nameWidth - self.moveStep * self.lbCurrentIndex +
                             self.spacing * (1 + self.isAllOut), 35, self.lbStr)
        else:
            painter.drawText(0, 54, self.lbStr)
            
        #print("paintEvent")
        
if __name__ == "__main__": 
    global  happyTime, lunchTime,lcdStyle,lbStrTemp,lbLunchStr,lbHappyStr,timeSpanInt
    happyTimeStr = getArgument("TimeSetting","happyTime")
    lunchTimeStr = getArgument("TimeSetting","lunchTime")
    lcdStyle = getArgument("TimeSetting","lcdStyle")
    lbStrTemp = getArgument("TimeSetting","lbStr")
    lbLunchStr = getArgument("TimeSetting","lbLunchStr")
    lbHappyStr = getArgument("TimeSetting","lbHappyStr")
    timeSpanInt = int(getArgument("TimeSetting","timeSpanInt"))
    happyTime = datetime.strptime(happyTimeStr, "%X")
    lunchTime = datetime.strptime(lunchTimeStr, "%X")

    app = QApplication(sys.argv)
    t = MyTimer()
    t.show()
    sys.exit(app.exec_())

