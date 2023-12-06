
#使用说明
##实现功能：server端和client端相互收发不同类型文件（txt\jpeg\doc\cpp\mp3\docx……）
##编译环境：vscode/cmd
##我写的server的ip:127.0.0.1 port：10086
##启动后，当链接成功建立，server端会有提示
##提示后 选择业务 （注意两边都要选，一收一发）
##需要传输的文件填绝对路径（不用双引号）
##收到的文件路径由os模块自动生成为当前工作目录
##此代码演示的是收txt文件，如要收取别的类型文件（txt\jpeg\doc\cpp\mp3\docx……），只需修改第47行文件后缀即可

import socket
import os  #os模块获取工作目录，避免文件传丢

# 用于从连接中接收文件
def receive(conn, filename):
    with open(filename, 'wb') as file:
        while True:
            data = conn.recv(1024)  # 接收文件数据，每次最多1024字节
            if not data:  # 如果没有接收到数据，则结束循环
                break
            file.write(data)  # 将接收到的数据写入文件

# 用于向连接中发送文件
def send(conn, filename):
    with open(filename, 'rb') as file:
        data = file.read(1024)  # 读取文件数据，每次最多读取1024字节
        while data:
            conn.send(data)  # 发送文件数据
            data = file.read(1024)  # 继续读取文件数据并发送


def main():
    udp_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建服务器socket
    udp_server.bind(('127.0.0.1', 10086))  # 绑定IP地址和端口号
    udp_server.listen(2)  # 开始监听，参数是最大连接数

    print("等待客户端连接...")
    udp_client, addr = udp_server.accept()  # 接受客户端连接
    print(f"连接来自: {addr}")
    
    #v表选项，表示是否需要发文件功能
    v = int( input("选择业务 1(send)/2(receive):") )#判断条件强制规定为int类
    if v==1:
        filename=input("文件名称（绝对路径）:")
        send(udp_client, filename)  # 发送文件给客户端
        print("文件传输完成")
    
    if v==2:
        # 动态获取当前工作文件路径，接收来自客户端的文件到工作文件夹 
        script_directory = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本的目录
        file_path = os.path.join(script_directory, 'recive.txt')  # 构建文件路径，给文件取名recive.txt(可更改)
        receive(udp_client, file_path)  
        print("收到来自用户的文件recive")

    udp_client.close()  # 关闭客户端连接
    udp_server.close()  # 关闭服务器socket

if __name__ == "__main__":
    main()

