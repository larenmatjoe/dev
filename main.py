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
            if packet.haslayer(sc.IP) and (packet.haslayer(sc.TCP) or packet.haslayer(sc.UDP)):
                ip = packet[1].src
                port = packet[2].dport
                print(packet[1].src, packet[1].dst)
                if int(port) > 2000:
                    continue
                array.append([ip,port])
        packet = None
        if len(array) != 0:
            pass
            #dataBase.databaseConnection(array)

    def monitorConnections():
        collection = []
        pointer = 0
        global flag
        while flag:
            packet = sc.sniff(count = 20, timeout = 5)
            collection.append(threading.Thread(target = deepPacket.filterConnection, args = (packet,) ))
            collection[pointer].start()
            pointer+=1
            if (pointer == 15):
                pointer = 0 
                collection.clear()
some = threading.Thread(target = deepPacket.monitorConnections, args = "")
some.start()
value = input("")
flag = False
some.join()
