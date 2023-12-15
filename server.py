import socket
import sqlite3
import threading
import time

flag = True

def authData(ip,port,username,password):
    db = sqlite3.connect("data.db")
    cur = db.cursor()
    global flag
    try:
        if flag:
            cur.execute("create table auth(ip varchar(15), port int(4), username varchar(30), password varchar(60));")
            db.commit()
            flag = False
    except:
        flag = False
    cur.execute(f"insert into auth values(\"{ip}\",22,\"{username}\",\"{password}\");")
    db.commit()
    db.close()

class server:
    def telnet() :
        #ip = "127.0.0.1"
        server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        server.bind(("",2323))
        server.listen(2)
        while True:
            #server.listen(3)
            connection, address = server.accept()
            connection.send(b"Welcome to Telnet Server \n")
            connection.send(b"======================== \n")
            connection.send(b"Username: ")
            username = connection.recv(1024)
            connection.send(b"Password: ")
            password = connection.recv(2048)
            time.sleep(2.5)
            username = username.strip()
            password = password.strip()
            username = username.decode()
            password = password.decode()
            authData(address[0],address[1],username,password)
            if username not in ["admin","Admin","root","administrator"]:
                connection.send(b"Connection revoked: INVALID UESRNAME")
            else:
                connection.send(b"Connection refused : WRONG PASSWORD")
            connection.shutdown(socket.SHUT_RDWR)
            connection.close()
server.telnet()
