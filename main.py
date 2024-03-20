import socket
import threading
import pygame

PORT = 6040
HEADER = 1024
FORMAT = 'utf-8'
DISCONNECT_MSG = "disc"

pygame.init()

SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)
server.listen()

clients = []

def handle_client(conn, addr, clients):
    print(f"{addr} connected\n")
    clients.append(conn)  # Добавляем нового клиента в список
    connected = True
    while connected:
        msg = conn.recv(HEADER).decode(FORMAT)
        if msg == "change":
            # Отправляем сообщение "change" всем клиентам, кроме отправителя
            for client in clients:
                if client != conn:
                    client.send(msg.encode(FORMAT))
                    print("sentfromserver")
        elif msg and msg != DISCONNECT_MSG:
            print(f"{addr}: {msg}")
        else:
            connected = False
            clients.remove(conn)
            conn.close()
            print(f"{addr} disconnected")
def start_server():
    while True:
        conn, addr = server.accept()
        clients.append(conn)
        thread = threading.Thread(target=handle_client, args=(conn, addr, clients))
        thread.start()
        print(f"{threading.active_count() - 1} active connections")

print(f"server is running on {SERVER}")
start_server()
