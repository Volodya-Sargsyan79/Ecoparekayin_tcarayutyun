import socket

from gps_server.settings import *
from gps_server.handlers.imei_handler import IMEIHandler


HOST = "0.0.0.0"
PORT = 5027


server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((HOST, PORT))
server.listen()

print(f"Listening on {HOST}:{PORT}")


while True:

    client, address = server.accept()

    print(address)

    data = client.recv(1024)

    imei_length = int.from_bytes(data[:2], "big")

    imei = data[2:2 + imei_length].decode()

    print(imei)

    if IMEIHandler.authenticate(imei):
        print("Device Authorized")
        client.send(b"\x01")
        client.close()
    else:
        print("Unknown Device")
        client.close()