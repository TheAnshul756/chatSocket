import socket
mysocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
mysocket.connect(('',2354))
mysocket.send("Hey There! This is a message which I am sending.")
print (mysocket.recv(2048))
mysocket.close()