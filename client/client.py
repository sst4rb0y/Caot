# coding : utf-8

import socket
import threading
from time import ctime
from tkinter import *
from PySide2.QtCore import QFile, Signal, QObject, Qt
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication, QMessageBox


class Signals(QObject):
	# 自定义一个信号
    mess = Signal(str)


class LoginWindow:
    
    def __init__(self):
        # 打开并读取当前文件夹下的ui文件夹下的main.ui设计文件
        qfile = QFile("ui/login.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()

        # 使用QUiLoader加载器实例中的load方法加载ui文件，返回其窗口的对象
        self.ui = QUiLoader().load(qfile)
        
        # 监听
        self.ui.login_button.clicked.connect(self.login_handler)

        # 使窗口可见
        self.ui.show()


    def login_handler(self):

        server_ip = self.ui.serverAddr_text.toPlainText()
        username = self.ui.username_text.toPlainText()

        if len(server_ip) <= 0 or len(username) <= 0:
            QMessageBox().about(self.ui, "错误", "请输入正确的地址与用户名！")
            return

        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            server_socket.connect((server_ip, 46875))
            QMessageBox().about(self.ui, "登录", "登录成功！")

            # 隐藏窗口
            self.ui.hide()

            # 进入主界面
            chatWindow = ChatWindow(
                account={
                    'username': username,
                    'server_ip': server_ip,
                    'server_port': 46875,
                    'server_socket': server_socket,
                }
            )

        except Exception as e:
            QMessageBox().about(self.ui, "错误", "连接失败，请稍后重试...")
            print(e)


class ChatWindow:
    
    def __init__(self, account : dict):

        # 保存账号信息
        self.account = account
        self.mess = []
        self.signals = Signals()        

        # 打开并读取当前文件夹下的ui文件夹下的main.ui设计文件
        qfile = QFile("ui/chat.ui")
        qfile.open(QFile.ReadOnly)
        qfile.close()

        # 使用QUiLoader加载器实例中的load方法加载ui文件，返回其窗口的对象
        self.ui = QUiLoader().load(qfile)
        
        # 监听发送按钮
        self.ui.send_button.clicked.connect(self.send_handler)
        self.signals.mess.connect(self.deal_mess)

        self.ui.info_label.setText('用户名: ' + account['username'] + ' 服务器地址: ' + account['server_ip'])

        # 接收服务器消息
        t = threading.Thread(target=ChatWindow.recev_mess, args=(self,))
        t.start()

        # 使窗口可见
        self.ui.show()


    def send_handler(self):
        
        message_edit = self.ui.edit_text.toPlainText()
        print('SEND MESSAGE: ' + message_edit)

        self.account['server_socket'].send(('[' + ctime() + '] '+ self.account['username'] + ': ' + message_edit).encode('utf-8'))
        self.ui.edit_text.setPlainText('')
    

    def deal_mess(self, str):
        self.mess.append(str)
        print('RECEV MESSAGE: ' + str)
        self.ui.message_text.setPlainText('\n'.join(self.mess))


    def recev_mess(self):
        while True:
            try:
                date = self.account['server_socket'].recv(1024)
                if not date:
                    self.signals.mess.emit("失去连接...")
                    break
                self.signals.mess.emit(date.decode('utf-8'))
            except Exception as e:
                self.signals.mess.emit("失去连接...")
                print(e)
                break



def main():

    # 实例化QT的应用，可以认为它要处理很多东西
    app = QApplication([])

    # 实例化主窗口类，东西都封装好了，会自动初始化
    loginWindow = LoginWindow()
    
    # 阻塞地等待监听
    app.exec_()





if __name__ == '__main__':
    main()


