import socket
import paramiko
import sqlite3
import threading
import time

flag = True
ip_addr = 'UNKNOWN'
def authData(ip,port,username,password):
    db = sqlite3.connect("data.db")
    cur = db.cursor()
    print(f"IP : {ip} PORT : {port} Username : {username} PASS : {password}")
    cur.execute(f"insert into auth values(\"{ip}\",{port},\"{username}\",\"{password}\");")
    db.commit()
    db.close()


def check_auth(username, password):
   # print("[+] Connection to SSH : ",username,password,'\n')
    authData(ip_addr,22,username,password)
    return True

# Create an SSH server
class MySSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        if check_auth(username, password):
            return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return "password"


class server:           #telnet server 
    def telnet() :
        try:
            server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            server.bind(("",2323))
            while flag:
                server.listen(3)
                connection, address = server.accept()
                connection.send(b"Welcome to Telnet Server \n")
                connection.send(b"======================== \n")
                connection.send(b"Username: ")
                username = connection.recv(1024)
                connection.send(b"Password: ")
                password = connection.recv(2048)
                time.sleep(0.5)
                username = username.strip()
                password = password.strip()
                username = username.decode()
                password = password.decode()
                authData(address[0],address[1],username,password)
                if username not in ["admin","Admin","root","administrator"]:
                    connection.send(b"Connection revoked: INVALID UESRNAME")
                    connection.close()
                else:
                    connection.send(b"Connection refused : WRONG PASSWORD")
                    connection.shutdown(socket.SHUT_RDWR)
                    connection.close()
        except:
            print("Port Scan Detected \n")
            server.telnet()

def ssh_server_start():
    # Create a socket to listen for incoming SSH connections
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(("", 2222))  # Change the IP and port as needed
    server_socket.listen(5)
    print("Listening for SSH connections on port 22...")
    global ip_addr
    while flag:
        try:
            client_socket, addr = server_socket.accept()
            ip_addr = addr[0]
            transport = paramiko.Transport(client_socket)
            transport.set_gss_host(socket.getfqdn(""))
            server = MySSHServer()
            transport.add_server_key(paramiko.RSAKey(filename="key_rsa"))
            #transport.add_server_key(paramiko.RSAKey.generate(1024))
            transport.start_server(server=server)
            chan = transport.accept(20)
            print("SSH negotiation failed.")
            transport.close()
        except EOFError or ConnectionResetError:
            pass

try:
   db = sqlite3.connect("data.db")
   cur = db.cursor()
   cur.execute("create table auth(ip varchar(15), port int(4), username varchar(30), password varchar(60));")
   db.commit()
   db.close()
except:
    pass

t = threading.Thread(target = server.telnet, args = "")   #creating a new thread for telnet sever
t1 = threading.Thread(target = ssh_server_start, args = "")     #creating ssh thread
t.start()
t1.start()
value = input("")
flag = False
t.join()
t1.join()
