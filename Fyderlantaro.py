from ftplib import FTP
import time
import platform
import os


if platform.system() == 'Windows':
    clear = 'cls'
else:
    clear = 'clear'

print("欢迎使用 Fyderlantaro | Powered by FriendShip Studio")
print("[C] FriendShip Studio 2021     All rights reserved.")
server_address = input("请输入FTP服务器地址:\n")

ctrl = True
while ctrl == True:
    try:
        server_port = int(input("请输入服务器的端口:\n"))
        ctrl = False
    except TypeError:
        print("错误的端口数据，请重新输入")

username = input("请输入服务器登录用户名:\n")
password = input("请输入服务器登录密码:\n")

ftp = FTP()
ftp.set_debuglevel(0)

try:
    ftp.connect(server_address, server_port)
    ftp.login(username, password)
except OSError:
    print("ERROR======================================================")
    print("[WARN] 无法连接至服务器")
    print("ERROR=======================================================")
    exit(0)
except TimeoutError:
    print("ERROR======================================================")
    print("[WARN] 服务器响应超时")
    print("ERROR=======================================================")
    exit(0)
except:
    print("ERROR======================================================")
    print("[WARN] 未知错误")
    print("ERROR=======================================================")
    exit(0)

print("============================================================")
print("[INFO] 成功与服务器建立连接")
print("============================================================")
time.sleep(1.0)
ftp.encoding = 'utf-8'

files = ftp.nlst()

ctrl = True
while ctrl == True:
    print("输入 'cd [目录名]' 可切换到此目录(输入..返回最上级)\t输入 'clone [文件名]' 可下载单一文件")
    print("输入 'cldir [目录名]' 可下载该目录下所有文件\t输入 'quit' 退出程序")
    print("输入 'lstdir' 可显示当前目录下的全部文件\t输入 'help' 刷新本页面")
    branch = input(f"您当前的FTP工作目录在 {ftp.pwd()}\t请键入命令:\n")

    if branch == 'lstdir':
        os.system(clear)
        if files == []:
            print(f"在 {ftp.pwd()} 下没有文件")

        print(f"在 {ftp.pwd()} 有以下文件:")
        for file in ftp.nlst():
            print(file)
    elif branch == 'help':
        os.system(clear)
        continue
    elif branch == 'quit':
        os.system(clear)
        print("感谢使用Fyderlantaro | 欢迎访问 https://github.com/FriendShip-Code-Studio")
        time.sleep(3)
        exit(0)
    elif branch.startswith("cd "):
        ch_dir = branch[3:]
        try:
            ftp.cwd(ch_dir)
        except:
            print("切换目录失败，是否键入正确目录名?")
            continue
        print(f"你成功地切换到{ftp.pwd()}")
    elif branch.startswith("clone "):
        selfile = branch[6:]
        try:
            print(f"[INFO] 正在尝试获取 {selfile} ...")
            f = open(selfile, 'wb')
            ftp.retrbinary(f"RETR {selfile}", f.write)
            f.close()
        except:
            print("获取文件失败，是否键入正确的文件名?")
            continue
        print(f"文件已成功保存于程序根目录下")
    elif branch.startswith("cldir "):
        cl_dir = branch[6:]
        try:
            ftp.cwd(cl_dir)
            os.makedirs(cl_dir)
            os.chdir(cl_dir)
            files = ftp.nlst()
            if files != []:
                for file in files:
                    print(f"[INFO] 正在尝试获取 {file} ...")
                    f = open(file, 'wb')
                    ftp.retrbinary(f"RETR {file}", f.write)
                    f.close()
                    ftp.cwd(".")
            os.chdir(".")
        except:
            print("下载目录失败，是否键入正确目录名?")
            continue

ftp.quit()
