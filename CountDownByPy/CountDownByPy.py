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

    def __init__(self, parent = None):
        super(MyTimer, self).__init__(parent)   
        self.resize(200, 80)   
        self.setWindowTitle("QTimerDemo")
        self.lb1 = QLabel('111111！',self)

        self.lcd = QLCDNumber(self)   
        self.lcd.setDigitCount(8)#所显示的位数   
        self.lcd.setMode(QLCDNumber.Dec)#十进制
        self.lcd.setSegmentStyle(QLCDNumber.Flat)
        self.lcd.display(time.strftime("%X",time.localtime()))
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
        happyTimeStr = getArgument("TimeSetting","happyTime")
        lunchTimeStr = getArgument("TimeSetting","lunchTime")
        happyTime = datetime.strptime(happyTimeStr, "%X")
        lunchTime = datetime.strptime(lunchTimeStr, "%X")

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
        print(f"{hour}小时{minu}分{seconds%60}秒")
        self.lcd.display(f"{hour}:{minu}:{seconds%60}")
        #self.lcd.display(time.strftime("%X",time.localtime()))
 

        
    #if __name__ == "__main__": 
app = QApplication(sys.argv)
t = MyTimer()
t.show()
sys.exit(app.exec_())

