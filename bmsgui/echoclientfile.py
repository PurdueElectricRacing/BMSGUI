from contextlib import closing
import socket

def client():
    HOST = socket.gethostname()
    PORT = 1090
    with closing(socket.socket()) as s:
        s.connect((HOST, PORT))
        i = raw_input("Filename: ")
        with open(i, 'r') as f:
            line = f.readline()
            while line:
                s.sendall(line)
                line = f.readline()
                data = s.recv(1024)
                print repr(data)

if __name__ == '__main__':
    client()