import socket
import threading


def handle_client(client_conn, client_addr):
    print(f"[Relai1] Nouveau client connecté : {client_addr}")

    try:
        full_msg = client_conn.recv(1024).decode()
        print(f"[Relai1] Message brut : {full_msg}")

        split_index = full_msg.find("),")
        if split_index == -1:
            raise ValueError("Format de message invalide")


        target_str = full_msg[:split_index + 1]
        client_msg = full_msg[split_index + 2:].strip()


        target_tuple = eval(target_str)
        if not (isinstance(target_tuple, tuple) and len(target_tuple) == 2):
            raise ValueError("Adresse invalide")

        target_ip, target_port = target_tuple
        print(f"[Relai1] Redirection vers {target_ip}:{target_port}")


        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.connect((target_ip, target_port))
        server_socket.send(client_msg.encode())


        server_response = server_socket.recv(1024).decode()
        print(f"[Relai1] Réponse du serveur : {server_response}")


        client_conn.send(server_response.encode())

        server_socket.close()
        client_conn.close()
        print(f"[Relai1] Terminé avec {client_addr}")

    except Exception as e:
        error_msg = f"[Relai1] Erreur : {e}"
        print(error_msg)
        client_conn.send(error_msg.encode())
        client_conn.close()


def start_relay():
    relay_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    relay_socket.bind(('127.0.0.1', 2001))
    relay_socket.listen()
    print("[Relai1] En attente de connexions clients...")

    while True:
        client_conn, client_addr = relay_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_conn, client_addr))
        thread.start()
        print(f"[Relai1] Nombre de threads actifs : {threading.active_count() - 1}")


if __name__ == "__main__":
    start_relay()
