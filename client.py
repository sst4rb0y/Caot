# coding : utf-8


import socket
import threading
from time import ctime
from tkinter import *
from time import sleep

mess_text = None
client = None
send_text = None

# server_ip = input('请输入服务器IP:\n')
# server_port = int(input('请输入服务器端口号:\n'))
server_ip = '101.34.188.210'
server_port = 46875
username = input('请输入你的用户名:\n')[:8]

def link():
    global server_ip, server_port, username


    # 创建 socket 对象
    global client
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            client.connect((server_ip, server_port))
            print('连接成功')
            break
        except Exception as e:
            print(f'[{ctime()}] 连接失败，五秒后重试...')
            sleep(5)
            continue

    get_mess_thread = threading.Thread(target=get_mess, args=(client, server_ip, username))
    get_mess_thread.setDaemon(True)
    get_mess_thread.start()




def get_mess(client:socket, server_ip:str, username:str):
    global mess_text
    while True:
        try:
            date = client.recv(1024)
            if not date:
                print('[%s] 失去服务器的连接:%s ' % (ctime(), server_ip))
                break
            print(date.decode('utf-8'))
            mess_text.insert(END, date.decode('utf-8'))


        except Exception as e:
            print('会话出错:')
            print(e)
            break

    # 关闭连接
    client.close()
    exit(1)

def do_send_mess():
    global send_text, client
    m = send_text.get('0.0','end')
    client.send(f'[{ctime()}] {username}:{m}'.encode('utf-8'))
    send_text.delete('1.0','end')


def main():
    
    # 创建主窗口
    master = Tk()
    master.title('Caot聊天室')
    # 获取屏幕长宽
    screenwidth = master.winfo_screenwidth()
    screenheight = master.winfo_screenheight()
    # 设置主窗口的大小和位置变量
    main_height = 600
    main_width =500
    alignstr = '%dx%d+%d+%d' % (main_width, main_height,
                                (screenwidth-main_width)/2, (screenheight-main_height)/2)
    # 设置主窗口的大小和位置
    master.geometry(alignstr)
    # 设置主窗口大小不可改变
    master.resizable(height=0, width=0)

    # 消息文本框
    global mess_text
    mess_text = Text(master, wrap=CHAR)
    mess_text_scroll = Scrollbar(mess_text, width=15)

    mess_text.config(yscrollcommand=mess_text_scroll.set)
    mess_text_scroll.config(command=mess_text.yview)

    mess_text.place(x=5, y=5, anchor='nw', height=390, width=490)
    mess_text_scroll.pack(side=RIGHT, fill=Y)


    
    global send_text
    # 发送文本框
    send_text = Text(master, wrap=CHAR)
    send_text.place(x=5, y=405, anchor='nw', height=190, width=460)

    # 发送按钮
    send_button = Button(master, text='s\ne\nn\nd', command=do_send_mess)
    send_button.place(x=465, y=405, anchor='nw', height=190, width=30)
    
    link()

    # 控件监听
    master.mainloop()



if __name__ == '__main__':
    main()