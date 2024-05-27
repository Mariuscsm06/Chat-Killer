import os
import sys
import socket
import threading
import select


def create_fifo(fifo_path):
    if os.path.exists(fifo_path):
        os.remove(fifo_path)
    os.mkfifo(fifo_path)

def superviseur(pseudo, server_ip, server_port):
    fifo_path = f"/var/tmp/{pseudo}.fifo"
    log_path = f"/var/tmp/{pseudo}.log"
    cookie_file = f"var/tmp/{pseudo}/COOKIE.txt"
    create_fifo(fifo_path)
    open(log_path, "w").close()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect((server_ip, int(server_port)))
    print("Connecté au serveur.")

    server_socket.send(pseudo.encode())

    response = server_socket.recv(2048).decode()
    if response == "Connexion refusée":
        print(response + " car une partie est en cours...")
        server_socket.close()
        return

    fifo_fd = os.open(fifo_path, os.O_RDWR|os.O_CREAT )


    # Lancer le premier fork pour détacher le processus principal
    pid = os.fork()
    if pid > 0:
        sys.exit(0)

    os.setsid()


    output_terminal_pid = os.fork()
    if output_terminal_pid == 0:
        os.execlp("xterm", "xterm", "-e", f"tail -f {log_path}")
        sys.exit(0)

    input_terminal_pid = os.fork()
    if input_terminal_pid == 0:
        os.dup2(os.open("/dev/null", os.O_WRONLY), sys.stdout.fileno()) 
        os.dup2(os.open("/dev/null", os.O_WRONLY), sys.stderr.fileno()) 
        os.execlp("xterm", "xterm", "-e", f"cat > {fifo_path}")
        sys.exit(0)

    fds = [fifo_fd, server_socket.fileno()]
    
    # Lire les messages depuis le FIFO et envoyer au serveur
    while True:
        try:
            rlist, _, _ = select.select(fds, [], [])
            for fd in rlist:
                if fd == fifo_fd:  # Lire depuis le fifo
                    message = os.read(fifo_fd, 2048).decode().strip()
                    if message.lower() == "!exit":
                        break
                    server_socket.send(message.encode())
                elif fd == server_socket.fileno(): 
                    response = server_socket.recv(2048).decode()
                    # Vérifier si la réponse est vide avant d'écrire dans le fichier log
                    if response:
                        cleaned_response = response.strip()
                        with open(log_path, "a") as log_file:
                            log_file.write(cleaned_response + "\n")
                        sys.stdout.flush()
        except Exception as e:
            print("Erreur lors de la communication avec le serveur :", e)
            break

    os.close(fifo_fd)
    server_socket.close()

def main():
    if len(sys.argv) != 3:
        print("Usage:", sys.argv[0], "hote port")
        sys.exit(1)
    else:
        server_ip = sys.argv[1]
        server_port = sys.argv[2]

    try:
        pseudo = input("Entrez votre pseudo: ")
    except KeyboardInterrupt:
        print("\nDéconnexion.")
        sys.exit(0)

    superviseur(pseudo, server_ip, server_port)

if __name__ == "__main__":
    main()
