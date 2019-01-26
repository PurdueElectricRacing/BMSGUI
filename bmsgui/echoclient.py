from contextlib import closing
import socket

def client():
    HOST = socket.gethostname()
    PORT = 1090
    with closing(socket.socket()) as s:
        s.connect((HOST, PORT))
        while True:
            i = raw_input("Message: ")
            s.sendall(i)
            data = s.recv(1024)
            print repr(data)

if __name__ == '__main__':
    client()