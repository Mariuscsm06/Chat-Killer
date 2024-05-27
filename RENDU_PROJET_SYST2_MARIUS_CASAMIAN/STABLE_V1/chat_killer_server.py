import socket
import threading
import sys
import select


def main():
    host = '0.0.0.0'  
    port = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Serveur en écoute sur {host}:{port}")

    sockets_list = [server_socket]
    clients = {}

    while True:
        read_sockets, _, _ = select.select(sockets_list, [], [])
        
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                client_socket, client_address = server_socket.accept()
                print(f"Nouvelle connexion de {client_address}")
                
                # Recevoir et stocker le pseudo du client
                pseudo = client_socket.recv(2048).decode().strip()
                sockets_list.append(client_socket)
                clients[client_socket] = pseudo
                print(f"Pseudo du client {client_address}: {pseudo}")
            else:
                message = notified_socket.recv(2048).decode()
                if message:
                    pseudo = clients[notified_socket]
                    print(f"les pseudo: {pseudo}")
                    print(f"{pseudo}: {message}")
                    for client_socket in clients:
                        client_socket.send(f"{pseudo}: {message}".encode())
                else:
                    print(f"Connexion fermée de {clients[notified_socket]}")
                    sockets_list.remove(notified_socket)
                    del clients[notified_socket]
                    notified_socket.close()

if __name__ == "__main__":
    main()
