import socket
import threading
import sys
import select


partie = False

def privee_ou_public(message, dico_clients, dico_etats, sender_socket, sender_pseudo, admin):
    s = message.split(' ')
    if s[0][0] == "@":
        recipient_pseudo = s[0][1:]
        if recipient_pseudo in dico_clients.values():
            for client_socket, pseudo in dico_clients.items():
                if pseudo == recipient_pseudo:
                    client_socket.send(f"{sender_pseudo}: {' '.join(s[1:])}".encode())
        elif recipient_pseudo == admin:
            print(f"Message de {sender_pseudo} pour l'administrateur: {' '.join(s[1:])}")
        else:
            sender_socket.send("Le destinataire n'existe pas.".encode())
    else:
        for client_socket, pseudo in dico_clients.items():
            client_socket.send(f"{sender_pseudo}: {message}".encode())

def bannir_joueur(pseudo, sockets_clients):
    if pseudo in sockets_clients:
        socket_a_bannir = sockets_clients[pseudo]
        socket_a_bannir.close()
        del sockets_clients[pseudo]
        print(f"Le joueur {pseudo} a été banni.")
    else:
        print("Le joueur à bannir n'existe pas.")


def gestion_message_serveur(dico_etats, sockets_client):
    global partie
    while True:
        servlist, _, _ = select.select([sys.stdin], [], [])
        if sys.stdin in servlist:
            command = sys.stdin.readline().strip()
            if command == "!list":
                for pseudo, etat in dico_etats.items():
                    print(f"{pseudo}: {etat}")
            elif command == "!start":
                print("Début de la partie !!")
                partie = True
            elif "!ban" in command:
                t = command.split(' ')
                pseudo_a_bannir = t[0][1:]  
                bannir_joueur(pseudo_a_bannir, sockets_client)
            # il manque les deux autres commandes à savoir !forgive et !suspend
def main():
    global partie
    host = '0.0.0.0'  
    port = int(sys.argv[1])

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Serveur en écoute sur {host}:{port}")

    sockets_list = [server_socket]
    clients = {}
    etats = {}
    sockets_clients = {}  # Dictionnaire pour associer les pseudonymes aux sockets

    # Démarrer le thread pour gérer les commandes du serveur
    gestion_serveur_thread = threading.Thread(target=gestion_message_serveur, args=(etats,sockets_clients))
    gestion_serveur_thread.daemon = True
    gestion_serveur_thread.start()

    while True:
        read_sockets, _, _ = select.select(sockets_list, [], [])
        
        for notified_socket in read_sockets:
            if notified_socket == server_socket:
                if partie:
                    print("La partie à déja commencée !! connexion refusée")
                    client_socket, _ = server_socket.accept()
                    client_socket.send("Connexion refusée".encode())
                    client_socket.close()
                else:
                    client_socket, client_address = server_socket.accept()
                    print(f"Nouvelle tentative de connexion de {client_address}")

                    # Recevoir et stocker le pseudo du client
                    pseudo = client_socket.recv(2048).decode().strip()
                    sockets_list.append(client_socket)
                    clients[client_socket] = pseudo
                    etats[pseudo] = "vivant"
                    sockets_clients[pseudo] = client_socket 
                    print(f"Pseudo du client {client_address}: {pseudo}")
                    client_socket.send("Connexion acceptée".encode())

            else:
                try:
                    message = notified_socket.recv(2048)
                    if message:
                        sender_pseudo = clients.get(notified_socket)
                        if sender_pseudo:
                            print(f"{sender_pseudo}: {message.decode()}")
                            privee_ou_public(message.decode(), clients, etats, notified_socket, sender_pseudo, "Admin")
                        else:
                            print("Erreur: Le pseudo associé à la socket n'a pas été trouvé.")
                except OSError as e:
                    # erreur dans le cas ou l'utilisateur banni tente d'écrire dans son terminal
                    disconnected_pseudo = clients.get(notified_socket)
                    if disconnected_pseudo:
                        print(f"Connexion fermée de {disconnected_pseudo}")
                        etats[disconnected_pseudo] = "mort"
                        sockets_list.remove(notified_socket)
                        del clients[notified_socket]
                        if disconnected_pseudo in sockets_clients:
                            del sockets_clients[disconnected_pseudo]  # Supprimer l'association
                        notified_socket.close()
                    else:
                        print("Erreur: Le pseudo associé à la socket n'a pas été trouvé.")



if __name__ == "__main__":
    main()
