from contextlib import closing
import socket

def server():
    HOST = socket.gethostname()
    PORT = 1090
    with closing(socket.socket()) as s:
        s.bind((HOST, PORT))
        s.listen(5)
        conn, addr = s.accept()
        with closing(conn):
            print 'Connected by', addr
            while True:
                data = conn.recv(1024)
                if data == 'END':
                    break
                if data:
                    print data
                conn.sendall(data)


if __name__ == '__main__':
    server()