"""
dict 客户端
发起请求，展示结果
"""

from socket import *
from getpass import getpass
ADDR=('127.0.0.1',8000)
#所有函数都用s
s=socket()
s.connect(ADDR)

def do_query(name):
    while True:
        word = input("单词：")
        if word =="##":#结束单词查询
            break
        msg="Q %s %s"%(name,word)
        s.send(msg.encode())
        data=s.recv(2048).decode()
        print(data)

def do_hist(name):
    msg="H %s"%name
    s.send(msg.encode())
    data = s.recv(128).decode()
    if data=="ok":
        while True:
            data=s.recv(1024).decode()
            if data=="##":
                break
            print(data)
    else:
        print("还没有历史记录")
#二级界面
def login(name):
    while True:
        print("""
        =================query========================
        1.查单词           2.历史记录             3.注销
        ==============================================
        """)
        cmd=input("输入选项：")
        if cmd =='1':
            do_query(name)
        elif cmd =="2":
            do_hist(name)
        elif cmd =='3':
            return
        else:
            print("请输入正确命令!")
#注册
def do_register():
    while True:
        name=input('User:')
        passwd=getpass()
        passwd1=getpass("Again:")

        if (" " in name) or (' ' in passwd):
            print("用户名与密码不能有空格")
            continue
        if passwd!=passwd1:
            print("两次密码不一致")
            continue

        msg = "R %s %s"%(name,passwd)
        #发送请求
        s.send(msg.encode())
        #接受反馈
        data=s.recv(128).decode()
        if data=="ok":
            print("注册成功")
            login(name)
        else:
            print("注册失败")
        return

#处理登录
def do_login():
    name=input("User:")
    passwd=getpass()
    msg="L %s %s"%(name,passwd)
    s.send(msg.encode())
    #等待反馈
    data=s.recv(128).decode()
    if data=="ok":
        print("登录成功")
        login(name)
    else:
        print("登录失败")
    return
#创建网络链接
def main():

    while True:
        print("""
        =================welcome================
        1.注册           2.登录             3.退出
        ========================================
        """)
        cmd=input("输入选项：")
        if cmd =='1':
            do_register()
        elif cmd =="2":
            do_login()
        elif cmd =='3':
            s.send(b'E')
            print("客户端退出")
            return
        else:
            print("请输入正确命令!")


if __name__=='__main__':
    main()