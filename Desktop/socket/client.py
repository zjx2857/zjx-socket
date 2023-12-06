
#使用说明
##实现功能：server端和client端相互收发不同类型文件（txt\jpeg\doc\cpp\mp3\docx……）
##编译环境：vscode/cmd
##我写的server的ip:127.0.0.1 port：10086
##启动后，当链接成功建立，server端会有提示
##提示后 选择业务 （注意两边都要选，一收一发）
##需要传输的文件填绝对路径（不用双引号）
##收到的文件路径由os模块自动生成为当前工作目录
##此代码演示的是收txt文件，如要收取别的类型文件（txt\jpeg\doc\cpp\mp3\docx……），只需修改第47行文件后缀即可

import socket #套接字
import os #动态获取工作目录（文件路径）
 

# 用于从连接中接收文件
def receive(conn, filename):
    with open(filename, 'wb') as file:#write
        while True:
            file_data = conn.recv(1024)  # 接收文件数据，每次最多1024字节
            if not file_data:  # 如果没有接收到数据，则结束循环
                break
            file.write(file_data)  # 将接收到的数据写入文件

# 用于向连接中发送文件
def send(conn, filename):
    with open(filename, 'rb') as file:#read
        file_data = file.read(1024)  # 读取文件数据，每次最多读取1024字节
        while file_data:
            conn.send(file_data)  # 发送文件数据
            file_data = file.read(1024)  # 继续读取文件数据并发送

def main():
    ip = input("请输入server ip:")
    port = int(input("请输入server port:"))#得强制类型转换为int，不然会报错

    udp_client =socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # 创建客户端socket
    udp_client.connect((ip, port))  # 连接服务器IP地址和端口号

    v = int( input("选择业务 1(send)/2(receive):") )#判断条件强制规定为int类
    if v==1:
        filename= input('文件名（绝对路径）:')
        send(udp_client, filename)  # 发送文件给服务器
        print("文件传输完成")
    if v==2:
        script_directory = os.path.dirname(os.path.abspath(__file__))  # 获取当前脚本的目录
        file_path = os.path.join(script_directory, 'recive.txt')  # 构建文件路径，给文件取名recive.txt(可更改)
        receive(udp_client, file_path)  # 接收来自服务器的文件
        print("收到来自服务器的文件recive")

if __name__ == "__main__":
    main()