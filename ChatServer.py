import socket
import select
import sys

class ChatServer:
    def __init__(self,port):
        self.usrname = {}
        self.port = port
        self.srvsock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
        self.srvsock.setsockopt( socket.SOL_SOCKET, socket.SO_REUSEADDR, 1 )
        self.srvsock.bind( ("", port) )
        self.srvsock.listen(5)
        self.descriptors = [self.srvsock]
        self.security_key= sys.argv[2]
        print ('ChatServer started on port %s' % port)
    def run(self):
        while 1:
            try:
                (sread,swrite,sexc) = select.select(self.descriptors,[],[])
                for sock in sread:
                    if sock == self.srvsock:
                        self.accept_new_connection()
                    else:
                        pstr = sock.recv(2048)
                        str1=pstr.decode('utf-8','strict')
                        if str1 == '':
                            host,port = sock.getpeername()
                            str1 = '%s left\n' %self.usrname[host+':'+str(port)]
                            self.broadcast_string(str1,sock)
                            sock.close()
                            self.descriptors.remove(sock)
                        else:
                            host,port = sock.getpeername()
                            newstr = '<%s> %s' % (self.usrname[host+':'+str(port)], str1)
                            self.broadcast_string( newstr, sock )
            except:
                print("Server Closed!!!")
                break
        self.srvsock.close()
    def accept_new_connection(self):
        newsock,(remhost,remport) = self.srvsock.accept()
        newsock.send(bytes("\r\nYou're connected to our ChatServer.\r\nInput your name and press enter.    ", "utf-8"))
        name = newsock.recv(2048).decode("utf8")
        name=name[0:-2]
        newsock.send(bytes("Now input security password\r\n", "utf-8"))
        passwd = newsock.recv(2048).decode("utf8")
        passwd = passwd[0:-2]
        # print(passwd)
        if passwd==self.security_key:
            newsock.send(bytes("You are now connected\r\n", "utf-8"))
            self.descriptors.append(newsock)
            # name = remhost+':'+str(remport)
            self.usrname[remhost+':'+str(remport)]=name
            str1 = '%s joined\r\n' %name
            # str1 = 'Client joined %s:%s\r\n' %(remhost,remport)
            self.broadcast_string(str1,newsock)
        else:
            newsock.send(bytes("Hold right there Sparky!! Wrong Password!! Connection not established. Try Again.\r\n", "utf-8"))
            newsock.close()
    def broadcast_string(self,str1,omit_sock):
        for sock in self.descriptors:
            if sock  != self.srvsock and sock != omit_sock:
                sock.send(bytes(str1, "utf8"))
        print(str1)

myServer = ChatServer(int(sys.argv[1]))
myServer.run()