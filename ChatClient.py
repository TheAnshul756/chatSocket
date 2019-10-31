import socket
import select
import sys
import getpass

class ChatClient:
    def __init__(self):
        self.cltsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.IP_add = sys.argv[1]
        self.port = int(sys.argv[2])
        self.cltsock.connect((self.IP_add,self.port))
        self.descriptors = [self.cltsock,sys.stdin]
    def run(self):
        self.process()
        self.getname()
        self.process()
        self.password_query()
        while 1:
            self.process()
    def process(self):
        (sread,swrite,sexc) = select.select(self.descriptors,[],[])
        for sock in sread:
            if sock == self.cltsock:
                msg = self.cltsock.recv(2048)
                print(msg.decode('utf-8','strict'))
            else:
                msg = sys.stdin.readline()
                self.cltsock.send(bytes(msg,'utf-8'))
                sys.stdout.write("<you> ")
                sys.stdout.write(msg)
                sys.stdout.flush()
    def getname(self):
        name = sys.stdin.readline()
        name=name+','
        self.cltsock.send(bytes(name,'utf-8'))
    def password_query(self):
        passwd = getpass.getpass()
        passwd=passwd+'##'
        # print(passwd)
        self.cltsock.send(bytes(passwd,'utf-8'))
myclient = ChatClient()
myclient.run()
