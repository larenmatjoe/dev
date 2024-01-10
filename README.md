
Requirements (python):
    -scapy
    -paramiko

# To Run

## Create virtual Env

python3 -m venv <name>
source <name>/bin/activate

## Install Requirements

pip3 install scapy paramiko

## Starting

### Starting Sniffing 

sudo python3 main.py

### Starting Server

python3 ser.py

## Accessing data

sqlite3 data.db

Table log contains incoming and outgoing IP log
Table auth contains username and password captured from server
