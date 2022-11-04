# coding : utf-8

import socket
import threading
from time import ctime
from config import BIND_PORT, MAX_CONNECT


group = []


def tcp_link(client_socket, ip_addr):
    global group
    print('新的连接:' + str(ip_addr))
    group.append([client_socket, ip_addr])
    client_socket.send('欢迎来到Caot聊天室!作者: YLCao\r\n'.encode('utf-8'))

    # 循环处理客户端请求
    while True:
        # 接受来自客户端数据
        date = client_socket.recv(1024)

        if not date:
            print('[%s] 连接断开:%s ' % (ctime(), str(ip_addr)))
            group.remove([client_socket, ip_addr])
            break

        print(date.decode('utf-8'))

        for i in group:
            try:
                i[0].send(date)
            except:
                pass
    
    client_socket.close()


def main():
    # 创建 socket 对象
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 监听
    server_socket.bind(("0.0.0.0", BIND_PORT))
    # 设置最大连接数，超过后排队
    server_socket.listen(MAX_CONNECT)
    # 循环建立新的连接
    print('服务器监听中...', "0.0.0.0:" + str(BIND_PORT), MAX_CONNECT)
    while True:
        try:
            # 建立客户端连接
            client_socket, ip_addr = server_socket.accept()
            t = threading.Thread(target=tcp_link, args=(client_socket, ip_addr))
            t.start()

        except Exception as e:
            print('回话出错:')
            print(e)
            break

    # 关闭连接
    server_socket.close()





if __name__ == '__main__':
    main()
