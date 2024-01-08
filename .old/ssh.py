import paramiko
import socket
import sqlite3
import threading
# ssh-keygen -t rsa -b 2048
# Define a function to handle authentication

flag = True
ip_addr = 'UNKNOWN'
def authData(username,password):
    db = sqlite3.connect("data.db")
    cur = db.cursor()
    global flag
    global ip_addr
    try:
        if flag:
            cur.execute("create table auth(ip varchar(15), port int(4), username varchar(30), password varchar(60));")
            db.commit()
            flag1 = False
    except:
        flag = False
    cur.execute(f"insert into auth values(\"{ip_addr}\",22,\"{username}\",\"{password}\");")
    db.commit()
    db.close()


def check_auth(username, password):
    print("[+] Connection to SSH : ",username,password,'\n')
    authData(username,password)
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

# Create a socket to listen for incoming SSH connections
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind(("0.0.0.0", 22))  # Change the IP and port as needed
server_socket.listen(5)

print("Listening for SSH connections on port 22...")
while True:
    client_socket, addr = server_socket.accept()
    ip_addr = addr[0]
    transport = paramiko.Transport(client_socket)
    transport.set_gss_host(socket.getfqdn(""))
    server = MySSHServer()
    transport.add_server_key(paramiko.RSAKey(filename="key_rsa"))
    #transport.add_server_key(paramiko.RSAKey.generate(1024))
    transport.start_server(server=server)

    chan = transport.accept(20)

    if chan is None:
        print("SSH negotiation failed.")
        transport.close()
    else:
        print("Authenticated!")

        # Handle the SSH session here
        chan.send("Welcome to my SSH server!\n")
        chan.send("Type 'exit' to close the connection.\n")

        while True:
            data = chan.recv(1024)
            if not data:
                break
            if data.strip() == "exit":
                break
            chan.send("You typed: " + data)

        chan.close()
        transport.close() 
