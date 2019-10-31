import socket
mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
mysocket.bind(('',2354))
mysocket.listen(5)
while 1:
    newsocket,(remhost,remport) = mysocket.accept()
    str=newsocket.recv(2048)
    newsocket.send(str)
    newsocket.close()
