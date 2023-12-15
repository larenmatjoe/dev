import scapy.all as sc
import socket
import threading
import sqlite3

flag = True
class dataBase:
    def databaseConnection(array):
        db = sqlite3.connect("data.db")
        cur = db.cursor()
        #        cur.execute("create table log(ip varchar(15), port int(4));")   #create new table if not exists
        try:
            for item in array:
                cur.execute(f"insert into log values(\"{item[0]}\",{item[1]});")
                print(item[0],item[1])
            db.commit() 
            db.close()
        except sqlite3.OperationalError:
            pass

class deepPacket:                       #packet monitoring class
    def filterConnection(packets):
        array = []
        for packet in packets:
            try:
                try:
                    ip = packet[1].src
                    port = packet[2].dport
                    array.append([ip,port])
                except AttributeError or ValueError:
                    pass
            except IndexError:
                pass
            packet = None
        dataBase.databaseConnection(array)

    def monitorConnections():
        collection = []
        pointer = 0
        try:
            try:
                while True:
                    packet = sc.sniff(count = 20, timeout = 5)      #sniffing packet using scapy till 20 packets or 5 seconds
                    collection.append(threading.Thread(target = deepPacket.filterConnection, args = (packet,) ))   #creating a new thread for packet classification
                    collection[pointer].start()  #starting thread
                    pointer+=1
                    if (pointer == 15):
                        pointer = 0 
                        collection.clear()
            except AttributeError:
                pass
        except ValueError:
            pass
try:
    deepPacket.monitorConnections()
except KeyboardInterrupt:
    exit(0)

