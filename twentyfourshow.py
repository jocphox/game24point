
from PyQt5 import QtWidgets
from PyQt5.QtCore import QStringListModel
from twentyfourui import Ui_MainWindow
import twentyfourcore as tf
import twentyfourdb as tfdb
import knowhow # 这是关于24点游戏的基本介绍；txt 转 py 文件
import howtoplay # 这是关于本插件的介绍； Txt 转 py 文件

class ShowMainWindow(QtWidgets.QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        # 初始化
        QtWidgets.QMainWindow.__init__(self,parent)
        # 调用父对象的设置方法，这才将所有的东西给传过来了
        self.setupUi(self)
        # 调用自身额外的一些操作，在QtDesigner中无法实现的操作在此处实现
        self.setup_UI()
        # 初始化，由于本次未封装DB，需要在打开的时候，生成DB文件，已进行查找
        a=tfdb.db()

        #翻译
    def switch2lv(self):
        self.listView.setVisible(True)
        self.textBrowser.setVisible(False)
        # self.verticalLayout.layoutStretch = (1, 1)
    def switch2tb(self):
        self.listView.setVisible(False)
        self.textBrowser.setVisible(True)
        # self.verticalLayout.layoutStretch = (1, 1)
    def setup_UI(self):
        self.switch2tb()
        self.showinfo("点击中部，获取问题；或者输入问题；获取答案；",1000000)
        self.textBrowser.setText(howtoplay.text)
        self.textBrowser.setStyleSheet("font-size:10pt;")
        self.pushButton.clicked.connect(self.loadQEasy)
        self.pushButton_2.clicked.connect(self.loadQNormal)
        self.pushButton_3.clicked.connect(self.loadQHard)
        self.pushButton_4.clicked.connect(self.loadanswer)
        self.pushButton_7.clicked.connect(self.knowhow)
        self.pushButton_8.clicked.connect(self.allquestions)
        self.pushButton_6.clicked.connect(self.myfavor)
        self.pushButton_5.clicked.connect(self.savefavor)
        self.listView.doubleClicked.connect(self.loadfromlv)

    def loadfromlv(self):
        self.loadQon(eval(self.listView.selectedIndexes()[0].data()))

    def loadQ(self,mode):
        question=eval(tfdb.db().getQ(mode))
        self.loadQon(question)
    def loadQon(self,qlst):
        self.lineEdit_7.setText(str(qlst[0]))
        self.lineEdit_8.setText(str(qlst[1]))
        self.lineEdit_9.setText(str(qlst[2]))
        self.lineEdit_10.setText(str(qlst[3]))

    def loadQEasy(self):
        self.loadQ('easy')
    def loadQNormal(self):
        self.loadQ('normal')
    def loadQHard(self):
        self.loadQ('hard')
    def loadanswer(self):
        self.switch2tb()
        try:
            question=[int(self.lineEdit_7.text()),int(self.lineEdit_8.text()),int(self.lineEdit_9.text()),int(self.lineEdit_10.text())]
            answer=tfdb.db().answer2(question)
            self.textBrowser.setText(answer)
            self.textBrowser.setStyleSheet("font-size:20pt;")
            self.showinfo("显示答案")
        except:
            self.textBrowser.setText(howtoplay.text)
            self.textBrowser.setStyleSheet("font-size:10pt;")


    def savefavor(self):
        try:
            question = (int(self.lineEdit_7.text()), int(self.lineEdit_8.text()), int(self.lineEdit_9.text()),
                            int(self.lineEdit_10.text()))
            if list(question) in tf.myFavor():
                tf.delFavor(question)
                self.myfavor()
                self.showinfo("取消收藏")
            else:
                tf.saveFavor(question)
                self.myfavor()
                self.showinfo("收藏成功")
        except:
            self.showinfo("收藏异常")
            self.myfavor()

    def showinfo(self,msg,stime=1000):
        self.statusbar.showMessage(msg,stime)

    def loadlv(self,lst):
        self.switch2lv()
        slm = QStringListModel()
        slm.setStringList(lst)
        self.listView.setModel(slm)
    def myfavor(self):
        self.loadlv(map(str,tf.myFavor()))
    def allquestions(self):
        self.loadlv(map(str,tfdb.db().getQs('all','qonly')))

    def knowhow(self):
        self.switch2tb()
        self.textBrowser.setText(knowhow.text)
        self.textBrowser.setStyleSheet("font-size:10pt;")

if __name__ == '__main__':
    import sys
    app = QtWidgets.QApplication(sys.argv)
    showWin = ShowMainWindow()
    showWin.show()
    sys.exit(app.exec_())