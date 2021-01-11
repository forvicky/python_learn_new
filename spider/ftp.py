import os
import ftplib


class Ftp():
    ftp = ftplib.FTP()

    def __init__(self, host, port=21):
        self.ftp.set_debuglevel(2)
        self.ftp.set_pasv(0)  # 0主动模式，1被动模式
        self.ftp.connect(host, port)

    def getwelcome(self):
        print(self.ftp.getwelcome())

    def getfilelist(self):
        list = self.ftp.nlst()  # 获得目录列表
        for name in list:
            print(name)  # 打印文件名字

    def mkd(self,pathname):
        self.ftp.mkd(pathname)

    def login(self, user, password):
        self.ftp.login(user, password)
        print(self.ftp.welcome)

    def upload_file(self, LocalFile, RemoteFile):
        print(LocalFile)
        if os.path.isfile(LocalFile) == False:
            raise "这不是一个合法的文件路径" + str(LocalFile)
        file_handler = open(LocalFile, "rb")
        self.ftp.storbinary('STOR '+RemoteFile, file_handler)
        file_handler.close()
        return

    def upload_file_tree(self, LocalDir, RemoteDir):
        if os.path.isdir(LocalDir) == False:
            raise "这不是一个合法的文件夹路径"+LocalDir
        LocalNames = os.listdir(LocalDir)
        self.ftp.cwd(RemoteDir)
        for Local in LocalNames:
            src = os.path.join(LocalDir, Local)
            if os.path.isdir(src):
                self.upload_file_tree(src, Local)
            else:
                self.upload_file(src, Local)

        self.ftp.cwd("..")
        return

    def close(self):
        self.ftp.quit()